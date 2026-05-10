#!/usr/bin/env python3
"""
Frida 17 + Android Java Hook 通用 runner 模板

特点：
  - 自动加载 frida_tools 自带的 java-bridge（解决 frida 17 Java undefined 问题）
  - 标准启动顺序：spawn → attach → create_script → load → resume
  - 支持 spawn 和 attach 两种模式
  - 自动检测 APP 崩溃 / 重启
  - 自动重连 hook
  - 完整 message handler（含 console.log）
  - 平稳常驻不退出

用法：
  1. 修改下方 CONFIG
  2. 把 hook 脚本路径填进 HOOK_SCRIPT
  3. python -u runner.py
  4. Ctrl+C 退出

依赖：
  pip install frida frida-tools
"""

import os, sys, time, threading, signal
from pathlib import Path
import frida


# =========================================================================
# CONFIG
# =========================================================================
DEVICE_ID    = 'c256d8fa'                            # adb devices 看到的 ID
TARGET_PKG   = 'com.luna.music'                      # 目标 APP 包名
HOOK_SCRIPT  = r'D:/tmp/hacker/Android/hooks/qishui-ad-bypass.js'
MODE         = 'attach'                              # 'spawn' or 'attach'
AUTO_RECONNECT = True                                # APP 崩溃时是否重连
JAVA_BRIDGE  = Path(frida.__file__).parent.parent / 'frida_tools' / 'bridges' / 'java.js'
# =========================================================================


# 全局事件
_stop = threading.Event()
_relaunch = threading.Event()


def on_message(msg, data):
    """frida script 消息回调"""
    t = msg.get('type')
    if t == 'send':
        payload = msg.get('payload')
        print(f'[send] {payload}', flush=True)
    elif t == 'log':
        lvl = msg.get('level', 'info')
        print(f'[{lvl}] {msg.get("payload")}', flush=True)
    elif t == 'error':
        print(f'[ERROR] {msg.get("description")}', flush=True)
        if msg.get('stack'):
            print(msg['stack'], flush=True)
    else:
        print(f'[?] {msg}', flush=True)


def on_detached(reason, *args):
    """session 断开回调"""
    print(f'\n[!] session detached: reason={reason}', flush=True)
    if reason in ('process-terminated', 'process-replaced', 'connection-terminated'):
        _relaunch.set()
    elif reason == 'application-requested':
        _stop.set()


def build_combined_source():
    """把 frida-java-bridge + 用户 hook 拼成一个 script"""
    bridge_src = JAVA_BRIDGE.read_text(encoding='utf-8')
    with open(HOOK_SCRIPT, 'r', encoding='utf-8') as f:
        hook_code = f.read()

    # bridge 是 IIFE 末尾把对象赋给 var bridge
    # 拼一句把 bridge 暴露到 globalThis.Java
    # 然后跑用户的 hook
    combined = '\n'.join([
        '// ========== java-bridge ==========',
        bridge_src,
        '',
        '// ========== expose Java ==========',
        "Object.defineProperty(globalThis, 'Java', { value: bridge, configurable: false, writable: false });",
        "console.log('[bridge] Java.available =', Java.available, ', Android', Java.androidVersion);",
        '',
        '// ========== user hook ==========',
        hook_code,
    ])
    return combined


def attach_or_spawn(device):
    """根据 MODE 决定 spawn 还是 attach"""
    pid = None

    if MODE == 'attach':
        for p in device.enumerate_processes():
            if TARGET_PKG.split('.')[-1] in p.name.lower() or '汽水' in p.name:
                pid = p.pid
                print(f'[*] attach mode: found {p.name} pid={p.pid}', flush=True)
                break
        if not pid:
            print(f'[!] APP not running, falling back to spawn', flush=True)
            return spawn_mode(device)
        return _do_attach(device, pid, is_spawn=False)

    elif MODE == 'spawn':
        return spawn_mode(device)

    else:
        raise ValueError(f'Unknown MODE: {MODE}')


def spawn_mode(device):
    pid = device.spawn([TARGET_PKG])
    print(f'[*] spawn mode: pid={pid}', flush=True)
    return _do_attach(device, pid, is_spawn=True)


def _do_attach(device, pid, is_spawn):
    """正确顺序：attach → create_script → load → resume"""
    session = device.attach(pid)
    print(f'[+] attached pid={pid}', flush=True)

    session.on('detached', on_detached)

    code = build_combined_source()
    print(f'[*] script size: {len(code)} bytes', flush=True)

    script = session.create_script(code)
    script.on('message', on_message)
    script.load()
    print(f'[+] script loaded', flush=True)

    if is_spawn:
        try:
            device.resume(pid)
            print(f'[+] resumed pid={pid}', flush=True)
        except Exception as e:
            print(f'[!] resume err: {e}', flush=True)

    return session, script


def main():
    print(f'=== frida hook runner ===', flush=True)
    print(f'  device: {DEVICE_ID}', flush=True)
    print(f'  pkg:    {TARGET_PKG}', flush=True)
    print(f'  hook:   {HOOK_SCRIPT}', flush=True)
    print(f'  mode:   {MODE}', flush=True)
    print(f'  auto-reconnect: {AUTO_RECONNECT}', flush=True)
    print(f'', flush=True)

    device = frida.get_device(DEVICE_ID, timeout=5)
    print(f'[*] connected: {device.name}', flush=True)

    while not _stop.is_set():
        _relaunch.clear()
        sess = None
        try:
            sess, scr = attach_or_spawn(device)
        except frida.ProcessNotFoundError as e:
            print(f'[X] process not found: {e}', flush=True)
            time.sleep(2)
            if not AUTO_RECONNECT: break
            continue
        except frida.InvalidArgumentError as e:
            print(f'[X] invalid arg (race?): {e}', flush=True)
            time.sleep(1)
            if not AUTO_RECONNECT: break
            continue
        except Exception as e:
            print(f'[X] attach failed: {type(e).__name__}: {e}', flush=True)
            time.sleep(2)
            if not AUTO_RECONNECT: break
            continue

        print(f'[*] hook running. ctrl-c to exit.', flush=True)

        # 阻塞直到 _relaunch 或 _stop
        try:
            while not _relaunch.is_set() and not _stop.is_set():
                time.sleep(0.5)
        except KeyboardInterrupt:
            _stop.set()

        try: sess.detach()
        except Exception: pass

        if _stop.is_set():
            break
        if AUTO_RECONNECT:
            print(f'[*] reconnecting in 2s...', flush=True)
            time.sleep(2)

    print(f'[*] exited cleanly', flush=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[*] user interrupted', flush=True)
