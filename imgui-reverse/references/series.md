# ImGui Reverse Series Notes

Total articles: 18

## 1. 1.ImGui-环境安装

- URL: https://jisuanjiwang.blog.csdn.net/article/details/150933835
- Description: æç« æµè§éè¯»1.5kæ¬¡ï¼ç¹èµ12æ¬¡ï¼æ¶è9æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imguiä¸è½½

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
IMGUI是一个被广泛应用到逆向里面的，它可以用来做外部的绘制，比如登录界面，内部绘制使用UE4和UE5，IMGUI结束后UE4和UE5就会写。这个有点麻烦，不过不要担心，抄我的代码，抄着抄着就会了，无需任何基础，只需要会抄就行，我怎么做你怎么做，代码的功能意思会写的很明白，就算写的不明白，直接把代码复制给ai，ai会给你解释清楚，无需担心学不会 
IMGUI，现在叫Dear ImGui，它是一个库，第一步要把它的源码下载下来 
 
 下载地址：https://github.com/ocornut/imgui 
  
 点击下图红框进行下载 
  
 下载完解压好，就得到了一个文件夹 
  
 然后下图红框的目录里都是会常用的 
  
 然后下图目录，是一些代码的写法实例 
 
 
然后绝大部分都是依赖，imgui提供的实例，就是把它的代码复制到我们需要的地方，所以要看它的实例，怎么看？双击下图红框，双击之后它会使用 Visual Studio 打开，Visual Studio安装看这里14.第二阶段x86游戏实战2-C++语言开发环境搭建-VisualStudio2017，文章里的百度网盘链接失效了，看主页置顶文章里的百度网盘链接 
 
双击打开之后，它可能会弹出下图的弹框，直接点确定就可以了，这里不点确定，后面要去解决方案的属性里设置，如果不设置会无法运行 
 
然后它就把所有的实例加载完成，如下图红框，下图红框这么多，看哪个？ 
 
看下图红框的directx11，directx是微软的也就是Windows操作系统的显卡绘制功能，它有跟多版本这用11版本，也就是directx11，使用directx11的代码我们就可以操作显卡绘制画面 
 
然后把它设置成启动项目 
 
然后点击下图红框运行 
 
下图红框位置是它可以实现的所有功能，可以点点看看，看到想要的就去找它的代码，然后把它的代码复制出来，它的东西很多，跟着我代码抄就可以了，不需要动脑子 
 
查看代码，首先查看main.cpp，直接鼠标左键双击打开它，main在程序中是入口的意思 
 
打开之后，就会给人一种这是什么，很陌生的感觉，完全看不懂，不知道是什么 
 
直接把main函数里的内容复制给ai，让ai写注释，如下ai写的说明，下一节将根据实例写代码

```text
// 程序入口函数：Windows 标准控制台/窗口程序的启动点
// 参数(int, char**)：默认的命令行参数，此处用不到但必须保留（Windows程序规范）
int main(int, char**)
{
    // ==============================================
    // 【逻辑阶段1：DPI适配初始化 → 解决高分辨率屏幕模糊问题】
    // 核心目标：让UI在不同清晰度屏幕（如1080P/4K/笔记本高分屏）上显示正常
    // 逻辑链：高DPI屏会自动缩放系统元素→若ImGUI不感知DPI→UI会模糊/偏小→先开启感知再获取缩放比例
    // ==============================================
    // 1. 启用ImGUI对Windows DPI的感知能力
    // 为什么要做：Windows系统在高DPI屏（如200%缩放）下，会对未开启DPI感知的程序强制拉伸→导致画面模糊
    // 作用：告诉ImGUI“当前屏幕有缩放”，后续UI绘制会基于缩放比例计算
    ImGui_ImplWin32_EnableDpiAwareness();

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
IMGUI是一个被广泛应用到逆向里面的，它可以用来做外部的绘制，比如登录界面，内部绘制使用UE4和UE5，IMGUI结束后UE4和UE5就会写。这个有点麻烦，不过不要担心，抄我的代码，抄着抄着就会了，无需任何基础，只需要会抄就行，我怎么做你怎么做，代码的功能意思会写的很明白，就算写的不明白，直接把代码复制给ai，ai会给你解释清楚，无需担心学不会 
IMGUI，现在叫Dear ImGui，它是一个库，第一步要把它的源码下载下来 
 
 下载地址：https://github.com/ocornut/imgui 
  
 点击下图红框进行下载 
  
 下载完解压好，就得到了一个文件夹 
  
 然后下图红框的目录里都是会常用的 
  
 然后下图目录，是一些代码的写法实例 
 
 
然后绝大部分都是依赖，imgui提供的实例，就是把它的代码复制到我们需要的地方，所以要看它的实例，怎么看？双击下图红框，双击之后它会使用 Visual Studio 打开，Visual Studio安装看这里14.第二阶段x86游戏实战2-C++语言开发环境搭建-VisualStudio2017，文章里的百度网盘链接失效了，看主页置顶文章里的百度网盘链接 
 
双击打开之后，它可能会弹出下图的弹框，直接点确定就可以了，这里不点确定，后面要去解决方案的属性里设置，如果不设置会无法运行 
 
然后它就把所有的实例加载完成，如下图红框，下图红框这么多，看哪个？ 
 
看下图红框的directx11，directx是微软的也就是Windows操作系统的显卡绘制功能，它有跟多版本这用11版本，也就是directx11，使用directx11的代码我们就可以操作显卡绘制画面 
 
然后把它设置成启动项目 
 
然后点击下图红框运行 
 
下图红框位置是它可以实现的所有功能，可以点点看看，看到想要的就去找它的代码，然后把它的代码复制出来，它的东西很多，跟着我代码抄就可以了，不需要动脑子 
 
查看代码，首先查看main.cpp，直接鼠标左键双击打开它，main在程序中是入口的意思 
 
打开之后，就会给人一种这是什么，很陌生的感觉，完全看不懂，不知道是什么 
 
直接把main函数里的内容复制给ai，让ai写注释，如下ai写的说明，下一节将根据实例写代码 

```text
// 程序入口函数：Windows 标准控制台/窗口程序的启动点
// 参数(int, char**)：默认的命令行参数，此处用不到但必须保留（Windows程序规范）
int main(int, char**)
{
    // ==============================================
    // 【逻辑阶段1：DPI适配初始化 → 解决高分辨率屏幕模糊问题】
    // 核心目标：让UI在不同清晰度屏幕（如1080P/4K/笔记本高分屏）上显示正常
    // 逻辑链：高DPI屏会自动缩放系统元素→若ImGUI不感知DPI→UI会模糊/偏小→先开启感知再获取缩放比例
    // ==============================================
    // 1. 启用ImGUI对Windows DPI的感知能力
    // 为什么要做：Windows系统在高DPI屏（如200%缩放）下，会对未开启DPI感知的程序强制拉伸→导致画面模糊
    // 作用：告诉ImGUI“当前屏幕有缩放”，后续UI绘制会基于缩放比例计算
    ImGui_ImplWin32_EnableDpiAwareness();

    // 2. 获取主显示器的DPI缩放比例（如1.0=100%、1.5=150%、2.0=200%）
    // 逻辑拆解：
    // - ::MonitorFromPoint(POINT{0,0}, MONITOR_DEFAULTTOPRIMARY)：
    //   找到屏幕左上角(0,0)坐标对应的显示器→若该位置无显示器（极端情况）→返回系统主显示器
    // - ImGui_ImplWin32_GetDpiScaleForMonitor(...)：
    //   从找到的显示器中读取系统设置的缩放比例→存入main_scale变量
    // 后续用途：窗口大小、UI元素（按钮/文字）都要乘以这个比例→保证不同DPI下显示效果一致
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY));

    // ==============================================
    // 【逻辑阶段2：创建Windows窗口 → 程序的“容器”】
    // 核心目标：生成一个可见的窗口，作为后续Direct3D渲染和ImGUI UI的载体
    // 逻辑链：Windows程序必须有窗口类→注册窗口类→用类创建窗口→无窗口则无法显示任何内容
    // ==============================================
    // 1. 定义“窗口类”（Windows系统的基础概念：相当于窗口的“模板”）
    // 为什么需要窗口类：Windows系统通过“窗口类”管理窗口的共性（如消息处理、图标、风格）
    // 每个字段的逻辑作用：
    WNDCLASSEXW wc = { 
        sizeof(wc),               // 【固定】告诉系统结构体大小→避免解析错误
        CS_CLASSDC,               // 【窗口风格】让窗口共享一个绘图上下文（DC）→Direct3D绘图需要
        WndProc,                  // 【核心】窗口消息处理函数→用户点击/关闭/键盘输入都靠它响应
        0L, 0L,                   // 【额外内存】暂时用不到→设为0
        GetModuleHandle(nullptr), // 【程序标识】获取当前程序的模块句柄→告诉系统“这个窗口属于哪个程序”
        nullptr, nullptr,         // 【图标/光标】暂时用系统默认→设为nullptr
        nullptr, nullptr,         // 【背景/菜单】暂时不需要→设为nullptr
        L"ImGui Example",         // 【类名】自定义标识→后续创建窗口要用到这个名字
        nullptr                   // 【扩展字段】暂时用不到→设为nullptr
    };

    // 2. 注册窗口类
    // 为什么要注册：把上面定义的“窗口类模板”告诉Windows系统→系统认可后才能用它创建窗口
    // 不注册的后果：调用CreateWindowW会失败→无法创建窗口
    ::RegisterClassExW(&wc);

    // 3. 用注册好的窗口类创建实际窗口
    // 逻辑拆解：传入窗口类名、标题、样式等参数→系统生成窗口并返回“窗口句柄”（hwnd，相当于窗口的ID）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,         // 【必传】用哪个窗口类创建（上面注册的“ImGui Example”）
        L"Dear ImGui DirectX11 Example", // 【窗口标题】显示在窗口顶部标题栏
        WS_OVERLAPPEDWINDOW,      // 【窗口样式】普通窗口（带标题栏、最小化/最大化/关闭按钮）
        100, 100,                 // 【初始位置】屏幕左上角x=100、y=100→避免窗口贴边
        (int)(1280 * main_scale), // 【窗口宽度】基础1280px × DPI缩放→高DPI屏窗口不会偏小
        (int)(800 * main_scale),  // 【窗口高度】基础800px × DPI缩放→和宽度逻辑一致
        nullptr, nullptr,         // 【父窗口/菜单】暂时没有→设为nullptr
        wc.hInstance,             // 【程序标识】当前程序模块句柄→和窗口类注册时一致
        nullptr                   // 【额外参数】暂时用不到→设为nullptr
    );

    // ==============================================
    // 【逻辑阶段3：初始化Direct3D → 给窗口装“绘图工具”】
    // 核心目标：创建Direct3D（微软的3D图形API）的设备和资源→后续ImGUI UI需要靠它渲染到窗口
    // 逻辑链：窗口是“容器”→需要Direct3D这个“画笔”→初始化失败则程序无法绘图→必须处理失败场景
    // ==============================================
    // 1. 调用自定义函数CreateDeviceD3D初始化Direct3D
    // 作用：创建Direct3D设备（g_pd3dDevice）、设备上下文（g_pd3dDeviceContext）、交换链（g_pSwapChain）
    // 这些是Direct3D绘图的核心资源→没有它们无法在窗口上画任何东西
    if (!CreateDeviceD3D(hwnd))  // 若初始化失败（返回false）
    {
        // 失败后必须清理：避免已创建的部分资源占用内存→导致内存泄漏
        CleanupDeviceD3D();      
        // 注销窗口类：系统已不会用这个类创建窗口→释放系统资源
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;                // 退出程序→返回1表示“运行失败”（0表示正常）
    }

    // ==============================================
    // 【逻辑阶段4：初始化ImGUI → 配置UI框架】
    // 核心目标：让ImGUI能和Windows窗口、Direct3D协同工作→后续能绘制UI
    // 逻辑链：ImGUI需要“上下文”（工作环境）→配置输入/风格→绑定Win32/Direct3D后端→否则无法使用
    // ==============================================
    // 1. 显示窗口（创建后默认是隐藏的→必须手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT); // SW_SHOWDEFAULT：系统默认方式显示（正常大小）
    ::UpdateWindow(hwnd);               // 强制刷新窗口→避免显示延迟（比如窗口卡在空白状态）

    // 2. 创建ImGUI上下文（ImGUI的“工作环境”）
    IMGUI_CHECKVERSION();        // 检查ImGUI版本→避免使用旧版本API导致兼容性问题
    ImGui::CreateContext();      // 初始化上下文→ImGUI所有功能都依赖这个上下文
    ImGuiIO& io = ImGui::GetIO(); // 获取ImGUI的IO对象→控制输入（键盘/鼠标）、帧率、字体等
    (void)io;                    // 避免“变量未使用”的编译警告（io后续会用到，此处先占坑）

    // 3. 配置ImGUI的输入功能
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard; // 启用键盘控制→按Tab切换UI、ESC关闭窗口
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;  // 启用手柄控制→支持游戏手柄操作UI

    // 4. 配置ImGUI的界面风格
    ImGui::StyleColorsDark();    // 使用深色主题（也可换ImGui::StyleColorsLight()浅色主题）
    // 为什么要选主题：默认主题可能不符合需求→提前配置减少后续修改

    // 5. 适配DPI：缩放ImGUI的UI元素
    ImGuiStyle& style = ImGui::GetStyle(); // 获取ImGUI的样式对象→控制UI大小、间距等
    style.ScaleAllSizes(main_scale);       // 缩放所有UI元素（按钮、文字、窗口边框）→和窗口DPI一致
    style.FontScaleDpi = main_scale;       // 单独缩放字体→避免文字模糊或大小不协调

    // 6. 绑定ImGUI的“后端”（关键步骤！连接ImGUI和系统/渲染API）
    ImGui_ImplWin32_Init(hwnd);            // Win32后端→让ImGUI能处理Windows消息（如鼠标点击）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext); // DX11后端→让ImGUI能通过Direct3D渲染

    // ==============================================
    // 【逻辑阶段5：定义程序状态变量 → 保存UI的动态数据】
    // 核心目标：存储UI的开关状态、颜色、计数器等→这些数据会在主循环中动态变化
    // 逻辑链：UI需要交互（比如点击按钮计数、勾选框开关窗口）→必须用变量保存状态→否则交互后数据丢失
    // ==============================================
    bool show_demo_window = true;   // 控制“ImGUI示例窗口”的显示/隐藏→初始为显示
    bool show_another_window = false;// 控制“自定义窗口2”的显示/隐藏→初始为隐藏
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色→初始为蓝灰色
    // 注：ImVec4是ImGUI的颜色类型→四个值分别是R（红）、G（绿）、B（蓝）、A（透明度），范围0.0f~1.0f

    // ==============================================
    // 【逻辑阶段6：主循环 → 程序的“心脏”（持续运行直到退出）】
    // 核心目标：无限循环处理消息、更新UI、渲染画面→程序才能响应用户操作并显示动态内容
    // 逻辑链：Windows程序是“事件驱动”→必须持续读取消息→处理消息后更新UI→渲染到屏幕→直到收到退出消息
    // ==============================================
    bool done = false; // 循环结束标志→初始为false（循环继续），收到退出消息后设为true
    while (!done)
    {
        // ----------------------------------------------
        // 【主循环子步骤1：处理Windows消息 → 响应用户操作】
        // 逻辑：Windows会把用户操作（点击、键盘、关闭）包装成“消息”→程序必须持续读取并处理→否则无响应
        // ----------------------------------------------
        MSG msg; // 存储单个Windows消息的结构体
        // ::PeekMessage：从系统消息队列中“读取并移除”所有待处理消息（PM_REMOVE=读取后删除）
        // 为什么用while循环：一次可能有多个消息（比如快速按多次键盘）→必须全部处理完
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg); // 转换消息（比如将“键盘按键码”转换为“字符”→方便处理输入）
            ::DispatchMessage(&msg);  // 分发消息→把消息传给窗口的消息处理函数（WndProc）
            if (msg.message == WM_QUIT) // 若收到“退出消息”（比如用户点击窗口关闭按钮）
                done = true; // 标记循环结束→下一轮循环会退出
        }
        if (done)
            break; // 退出主循环→进入后续清理阶段

        // ----------------------------------------------
        // 【主循环子步骤2：处理窗口遮挡 → 优化性能】
        // 逻辑：窗口被其他窗口完全遮挡时→渲染画面用户看不到→暂停渲染节省CPU/GPU资源
        // ----------------------------------------------
        // g_SwapChainOccluded：自定义变量→标记窗口是否被遮挡
        // g_pSwapChain->Present(0, DXGI_PRESENT_TEST)：测试交换链是否被遮挡→返回DXGI_STATUS_OCCLUDED表示遮挡
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10); // 休眠10毫秒→减少空循环消耗的CPU资源
            continue;    // 跳过本次循环的后续渲染步骤→直接进入下一轮
        }
        g_SwapChainOccluded = false; // 重置遮挡标志→窗口显示时恢复渲染

        // ----------------------------------------------
        // 【主循环子步骤3：处理窗口 resize → 适配窗口大小变化】
        // 逻辑：用户拖动窗口改变大小时→Direct3D的渲染资源（如渲染目标）也需要跟着变→否则画面会错位
        // 为什么不在WM_SIZE消息里直接处理：Direct3D资源调整需要先清理再重建→在消息处理里做可能导致渲染异常
        // 解决方案：用g_ResizeWidth/g_ResizeHeight标记需要调整→在主循环安全时机处理
        // ----------------------------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0) // 若标记了需要调整大小
        {
            CleanupRenderTarget(); // 先清理旧的渲染目标→避免资源冲突
            // 调整交换链大小→交换链是Direct3D显示画面的“缓冲区”→大小必须和窗口一致
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0; // 重置标记→避免重复调整
            CreateRenderTarget(); // 创建新的渲染目标→适配新窗口大小
        }

        // ----------------------------------------------
        // 【主循环子步骤4：ImGUI帧初始化 → 准备绘制UI】
        // 逻辑：ImGUI是“基于帧”的UI框架→每个帧都要重新初始化→才能收集最新输入、计算UI布局
        // 顺序不能乱：必须先初始化后端→再初始化ImGUI帧→否则UI会错乱
        // ----------------------------------------------
        ImGui_ImplDX11_NewFrame(); // DX11后端初始化帧→告诉Direct3D“准备好绘制ImGUI了”
        ImGui_ImplWin32_NewFrame(); // Win32后端初始化帧→收集当前鼠标/键盘输入→传给ImGUI
        ImGui::NewFrame();         // ImGUI核心帧初始化→后续所有UI绘制都必须在这之后

        // ----------------------------------------------
        // 【主循环子步骤5：绘制ImGUI UI → 核心交互部分】
        // 逻辑：用ImGUI的API创建窗口、按钮、文本等→每个UI元素都需要“Begin/End”包裹→形成独立区域
        // 交互逻辑：UI元素的状态（如按钮是否被点击、复选框是否勾选）会实时更新绑定的变量
        // ----------------------------------------------
        // 1. 显示ImGUI官方示例窗口（包含所有ImGUI功能演示→方便学习）
        if (show_demo_window) // 若show_demo_window为true→显示窗口
            // 传入&show_demo_window：窗口右上角的“关闭按钮”会直接修改这个变量→实现“关闭窗口”功能
            ImGui::ShowDemoWindow(&show_demo_window);

        // 2. 自定义窗口1：Hello World窗口（基础UI元素示例）
        {
            // static变量：在循环中保持值（普通变量每次循环都会重置→无法实现计数/滑块记忆）
            static float f = 0.0f;    // 滑块绑定的浮点值→初始0.0f
            static int counter = 0;   // 按钮点击计数器→初始0

            // 开始创建窗口：标题“Hello, world!”，后续UI都在Begin和End之间
            ImGui::Begin("Hello, world!"); 

            ImGui::Text("This is some useful text."); // 显示静态文本→无交互

            // 复选框：绑定show_demo_window变量→勾选/取消会直接修改变量值
            ImGui::Checkbox("Demo Window", &show_demo_window);
            // 复选框：绑定show_another_window变量→控制第二个窗口的显示
            ImGui::Checkbox("Another Window", &show_another_window);

            // 滑块：控制f的值→范围0.0f~1.0f→拖动滑块时f会实时更新
            ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
            // 颜色选择器：绑定clear_color变量→选择颜色时会实时修改窗口背景色
            ImGui::ColorEdit3("clear color", (float*)&clear_color);

            // 按钮：点击时返回true→触发counter加1
            if (ImGui::Button("Button"))
                counter++;
            ImGui::SameLine(); // 让下一个UI元素和按钮在同一行显示→避免换行
            ImGui::Text("counter = %d", counter); // 显示计数器当前值→实时更新

            // 显示帧率信息：io.Framerate是ImGUI自动计算的当前帧率→帮助调试性能
            ImGui::Text("Application average %.3f ms/frame (%.1f FPS)", 
                        1000.0f / io.Framerate, io.Framerate);

            ImGui::End(); // 结束窗口创建→必须和Begin配对→否则UI会错乱
        }

        // 3. 自定义窗口2：可关闭的简单窗口
        if (show_another_window) // 若变量为true→显示窗口
        {
            // Begin第二个参数传&show_another_window：窗口关闭按钮会修改这个变量
            ImGui::Begin("Another Window", &show_another_window);

            ImGui::Text("Hello from another window!"); // 静态文本

            // 按钮：点击时设show_another_window为false→关闭当前窗口
            if (ImGui::Button("Close Me"))
                show_another_window = false;

            ImGui::End(); // 结束窗口
        }

        // ----------------------------------------------
        // 【主循环子步骤6：渲染UI到Direct3D → 把UI转换成图像】
        // 逻辑：ImGUI的“绘制”只是生成绘图指令→需要Direct3D执行这些指令→才能在窗口上显示
        // ----------------------------------------------
        ImGui::Render(); // 生成ImGUI的绘图数据（DrawData）→包含所有UI的位置、颜色、形状

        // 计算背景色：乘以透明度（clear_color.w）→避免背景色过亮盖过UI
        const float clear_color_with_alpha[4] = { 
            clear_color.x * clear_color.w, 
            clear_color.y * clear_color.w, 
            clear_color.z * clear_color.w, 
            clear_color.w 
        };

        // 设置Direct3D的渲染目标→告诉Direct3D“要画到主窗口的渲染目标上”
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空渲染目标→用计算好的背景色填充窗口→避免上一帧的画面残留
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);

        // 执行ImGUI的绘图指令→通过Direct3D把UI画到渲染目标上
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // ----------------------------------------------
        // 【主循环子步骤7：显示画面到窗口 → 让用户看到UI】
        // 逻辑：Direct3D把UI画到“交换链”（后台缓冲区）→需要调用Present把后台缓冲区的画面显示到前台
        // ----------------------------------------------
        // g_pSwapChain->Present(同步参数, 标志)：
        // 第一个参数1：启用垂直同步（VSync）→帧率和显示器刷新率一致→避免画面撕裂
        // 第一个参数0：禁用垂直同步→帧率更高→但可能有画面撕裂
        HRESULT hr = g_pSwapChain->Present(1, 0);
        // 检查是否被遮挡→更新g_SwapChainOccluded变量→供后续性能优化使用
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // ==============================================
    // 【逻辑阶段7：清理资源 → 程序退出前释放内存/系统资源】
    // 核心目标：避免内存泄漏（已创建的资源不释放→系统内存被占用）
    // 逻辑链：创建资源的逆顺序→先清理ImGUI→再清理Direct3D→最后清理窗口→确保所有资源都被释放
    // ==============================================
    // 1. 清理ImGUI资源
    ImGui_ImplDX11_Shutdown();  // 关闭ImGUI的DX11后端→释放相关渲染资源
    ImGui_ImplWin32_Shutdown(); // 关闭ImGUI的Win32后端→释放消息处理资源
    ImGui::DestroyContext();    // 销毁ImGUI上下文→释放ImGUI的所有内存

    // 2. 清理Direct3D资源
    CleanupDeviceD3D();         // 调用自定义函数→释放Direct3D设备、交换链等

    // 3. 清理Windows窗口资源
    ::DestroyWindow(hwnd);      // 销毁窗口→释放窗口占用的系统资源
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance); // 注销窗口类→系统不再保留该类

    return 0; // 程序正常退出→返回0（Windows程序规范：0表示成功）
}

```

## 2. 2.ImGui-搭建一个外部绘制的窗口环境（使用ImGui绘制一个空白窗口）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/150962299
- Description: æç« æµè§éè¯»1.7kæ¬¡ï¼ç¹èµ48æ¬¡ï¼æ¶è18æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：1.ImGui-环境安装 
本章的步骤会有很多，不需要记住，会抄会用就行了别的真的不需要知道，知识很多不要把时间浪费在记这种无用知识，不要把时间浪费在去了解这种知识上，只需要记住在这里可以得到答案就行，本文章不会下线，忘了就回来看，知识很多千万不要浪废时间 
本次使用Visual Studio 2022上一个内容中有Visual Studio 2017的安装，2022和2017安装的步骤都一样，安装包在置顶文章的百度网盘里也有。 
首先打开 Visual Studio 2022，然后·点击下图红框的创建新项目，本章的代码说明，放到了最后，这之间的过程只需要抄就行（不抄会找不到文件），不需要关心代码有什么用，代码的用处说明全部都放到了最后 
 
选择下图红框的空项目，然后点击下一步 
 
然后输入一个项目名，然后点击创建，以后绘制的代码都写在它里面 
 
然后再看ImGui给的Directx11的实例，它加载了下图红框的文件，所以我们也要加载 
 
然后再回到我们刚创建的ImGuiOutTest项目里，如下图右击源文件，选择新建项 
 
创建一个main.cpp文件，然后点击添加 
 
添加好main.cpp后先给它里面添加下图红框的内容

```text
int main() {
	return 0;
}

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：1.ImGui-环境安装 
本章的步骤会有很多，不需要记住，会抄会用就行了别的真的不需要知道，知识很多不要把时间浪费在记这种无用知识，不要把时间浪费在去了解这种知识上，只需要记住在这里可以得到答案就行，本文章不会下线，忘了就回来看，知识很多千万不要浪废时间 
本次使用Visual Studio 2022上一个内容中有Visual Studio 2017的安装，2022和2017安装的步骤都一样，安装包在置顶文章的百度网盘里也有。 
首先打开 Visual Studio 2022，然后·点击下图红框的创建新项目，本章的代码说明，放到了最后，这之间的过程只需要抄就行（不抄会找不到文件），不需要关心代码有什么用，代码的用处说明全部都放到了最后 
 
选择下图红框的空项目，然后点击下一步 
 
然后输入一个项目名，然后点击创建，以后绘制的代码都写在它里面 
 
然后再看ImGui给的Directx11的实例，它加载了下图红框的文件，所以我们也要加载 
 
然后再回到我们刚创建的ImGuiOutTest项目里，如下图右击源文件，选择新建项 
 
创建一个main.cpp文件，然后点击添加 
 
添加好main.cpp后先给它里面添加下图红框的内容 
 

```text
int main() {
	return 0;
}

```
 
然后鼠标右击选择打开文件夹 
 
然后就能来到我们项目的文件目录里，如下图，下图是后补的所以有很多文件，跟着下方的步骤来就可以 
 
然后把ImGui的文件复制到我们的（ImGuiOutTest）项目里，把下图红框文件复制过去 
 
然后再把文件拖到源文件里 
 
拖完之后 
 
然后再把下图红框的4个文件复制到我们的项目里，复制之前为了好区分先创建一个ImGui的文件夹 
 
如下图创建ImGui文件夹 
 
然后把那4个文件夹都放进去 
 
复制完后来到vs2022里，如下图新建一个筛选器 
 
名字叫ImGui，如下图红框 
 
然后把这4个文件拖进去 
 
拖动完之后，就可以了 
 
然后开始复制代码，首先把下图红框的代码复制过去 
 
复制过来后，它就会报错，这是因为没有引入需要的文件 
 
然后再创建一个文件，如下图右击头文件，然后选择新建项 
 
然后如下图添加一个main.h文件 
 
创建完后 
 
然后在main.cpp添加下图红框的代码 #include "main.h" 
 
然后在main.h文件里添加 #include "windows.h" 
 
再回到main.cpp文件里，可以看到有些代码就不报错了 
 
然后鼠标左键单击下图红框位置，然后按F1 
 
就可以打开微软对于 WNDCLASSEXW 的说明，其它的说明比如 CreateWindowW 也是这样的看法，这说明看了也没用，能看懂的不用看，看不懂的不用看，跟着我的代码抄和描述来学就行了，不用管它，说明不是给新手看的 
 
然后点击下图红框 
 
可以查看第二个参数的说明和能写的值有哪些，如下图红框，看不懂就去问ai大模型 
 
然后还缺下图红框的代码 
 
然后来到ImGui的代码，按着CTRL键鼠标左键单机下图红框 
 
就可以跳转到WndProc函数里，把它们复制过去 
 
 
然后它就不会报错了，如下图红框，注意WndProc函数，要在main函数的上方，如果放到了main函数的下方，main函数里面它还是会找不到WndProc 
 
 
然后再把下图红框的三行代码复制一下 
 
 
复制到main.h里，可以看到它会报错，找不到文件 
 
 
因为它俩在ImGui筛选器里，如下图红框 
 
 
然后可以看到main函数里已经不报错了，但是WindProc函数里还有报错，所以接下来处理WindProc函数中的报错 
 
 
再来到ImGui的源码中，如下图红框位置创建了 ImGui_ImplWin32_WndProcHandler，所以要把它复制过去 
 
 
然后复制完就可以了，但还是有两个位置报错 g_ResizeWidth 和 g_ResizeHeight接下来找它们 
 
 
然后按着CTRL鼠标左键单机下图红框位置 
 
 
然后把下图红框位置的代码复制过去 
 
 
然后就不报错了，然后就可以注册一个窗口类，然后创建一个窗口了 
 
 
点击下图红框尝试运行 
 
 
然后它会报错，这里点击否 
 
 
错误说明是找不到imgui.h文件，然后双击下图红框任意一个 
 
然后它出错的文件是 imgui_impl_dx11.cpp，然后它在ImGui筛选器里，然后imgui.h在源文件筛选器里，解决这个文件就要设置包含目录 
 
如下图鼠标右击ImGuiOutTest，然后选择属性 
 
然后根据下图进行点击 
 
单击下图红框 
 
然后再单击下图红框 
 
然后找到imgui.h文件的目录，找到后点击选择文件夹 
 
如下图，然后点击确定 
 
然后点击应用，再点击确定，也可以直接点击确定（确定包含的应用） 
 
然后就不会报错了 
 
然后再次运行 
 
然后可以运行了，但是没有窗口，这样原因是，没有执行显示窗口，所以接下来继续复制代码 
 
然后创建D3D 
 
复制之后又有一大堆错误，这是因为缺少d3d的引入 
 
引入d3d，把下图红框的代码复制过去 
 
复制后 
 
然后还剩下图红框位置在报错，然后继续找它们 
 
然后把下图红框的代码复制过去 
 
然后下图红框位置就不报错了 
 
然后再把下图红框的代码复制过去 
 
然后下图黄框位置就不报错了 
 
然后再把下图红框位置复制过去 
 
然后还剩下图红框位置报错，接着找它们 
 
把下图红框的代码复制过去 
 
复制完就不报错了 
 
再次运行，它还会错误 
 
错误说明是无法解析的符号，双击也没有反应，这个错误是，我们只引用了d3d的声明（声明就是告诉我们有这样一个东西，但是东西在哪它不告诉我们），没有引入d3d的库（这个库是告诉我们东西在什么位置，声明和库是分开的，它俩配合起来才能正常运行）D3D的库需要我们自己手动引入 
 
鼠标右击选择属性 
 
然后找到链接器里的输入，然后在附加依赖项里写d3d11.lib;，然后点击确定 
 
为什么写d3d11.lib;，如下图来到ImGui的源码，然后右击 example_win32_directx11，然后选择属性 
 
然后如下图红框，它的链接器里的输入就写的d3d11.lib;，所以我们也写d3d11.lib; 
 
然后就可以运行了 
 
然后继续抄，直到抄到可以画出一个东西，然后该复制下图红框的代码了，它是来显示窗口了 
 
复制过来没有报错，如果复制后它是白色的，可以尝试把文件关闭重新打开，这是vs的问题，不用管 
 
然后继续抄 
 
它也没有报错 
 
然后继续 
 
它也没有报错 
 
然后继续 
 
然后也没有报错 
 
继续抄 
 
然后也没有报错 
 
继续抄，一个循环 
 
然后复制之后如下图红框 
 
然后再运行，可以看到一个卡死的白色的窗口了 
 
这个窗口是卡死的没法用然后继续抄，这是WIndows系统的消息循环，消息循环就是我们鼠标的移动，键盘的按下，都是一个消息循环中的消息，通过消息可以得到鼠标移动的位置，键盘按下的键等 
 
然后也没有报错 
 
继续复制 
 
然后这有报错了 
 
然后复制下图红框的代码 
 
复制完就不会报错了 
 
然后复制下图红框的内容 
 
复制之后 
 
再次运行，如下图可以得到一个蓝色背景的窗口了 
 
然后把下图红框的代码复制过去，这是运行完（关闭窗口）清理内存的代码 
 
 
到这就框架就复制完了，这时可以把这代码备份一下，后面想使用的时候直接拿过来，就不需要重新跟着上方的步骤来复制了 
main.cpp的完整代码 

```text
// 引入头文件：包含程序所需的基础定义（相当于画画前准备好颜料、画笔的说明书）
#include "main.h"

// ==============================================
// 【全局静态变量 → 跨函数共享的“画画工具/状态”】
// 小白类比：这些变量就像画室里的“画架尺寸”“画笔”“画布”，所有人都能用但不外借
// ==============================================
// 窗口需要调整的宽高：记录“画架要改成多大”（用户拖动窗口后，先记下来再调整）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// Direct3D核心“画画工具”（显卡提供的功能）：
static ID3D11Device* g_pd3dDevice = nullptr;          // 1. 颜料工厂：负责生产“能挂在画布上的颜料”（创建显卡资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 2. 画师的手：负责用颜料在画布上画画（执行渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;        // 3. 双画布切换器：后台画布画完→快速切换到前台展示（避免用户看到半成品）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 4. 带颜料层的画布（核心！）：专门用来画画，颜料能附着在上面
static bool                     g_SwapChainOccluded = false; // 画布是否被挡住：记录“观众看不到幕布”（窗口被遮挡）→暂停画画

// 【ImGUI窗口消息处理器 → 画师的助理：先处理简单需求】
// 小白类比：用户说“要画个圆”，助理先记下来，处理不了再找画师
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// ==============================================
// 【自定义窗口消息处理函数 → 画师的“需求接收台”】
// 小白类比：用户的所有要求（拖动画架、关闭画室）都先传到这，再安排处理
// ==============================================
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 第一步：助理先处理需求（比如用户点击画布上的按钮）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    switch (msg)
    {
    // 需求1：用户拖动画架边缘→画架变大/变小
    case WM_SIZE:
        // 若画架被收起来（窗口最小化）→不用调整画布
        if (wParam == SIZE_MINIMIZED)
            return 0;
        // 记录新的画架尺寸（宽=LOWORD(lParam)，高=HIWORD(lParam)→Windows规定的记法）
        g_ResizeWidth = (UINT)LOWORD(lParam); 
        g_ResizeHeight = (UINT)HIWORD(lParam);
        return 0;

    // 需求2：用户按ALT+空格→想调出画架菜单（禁用，避免干扰画画）
    case WM_SYSCOMMAND:
        if ((wParam & 0xfff0) == SC_KEYMENU) 
            return 0;
        break;

    // 需求3：用户要关门（关闭窗口）→通知画师停止工作
    case WM_DESTROY:
        ::PostQuitMessage(0); // 发“下班”通知→主循环收到后停止
        return 0;
    }

    // 处理不了的需求→交给“画室管理员”（Windows系统）默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// ==============================================
// 【创建渲染目标视图 → 制作“能挂住颜料的画布”】
// 小白重点！！！
// 核心概念类比：
// - 渲染目标（RenderTarget）= 带“颜料吸附层”的画布：普通白纸（缓冲区）不能直接画画，要涂一层特殊涂层（渲染目标视图），颜料才能粘住
// - 交换链（SwapChain）= 双画布切换器：有两块画布，一块在后台画画（后台缓冲区），一块在前台展示（前台缓冲区），画完后快速切换，用户看不到半成品
// 这一步就是：给后台画布涂“颜料吸附层”，让画师能在上面画画
// ==============================================
void CreateRenderTarget()
{
    // 1. 从“双画布切换器”（交换链）中拿出“后台画布”（空白白纸，类型是ID3D11Texture2D）
    ID3D11Texture2D* pBackBuffer; // 临时变量：存空白白纸
    // GetBuffer(0, ...)：拿第0块画布（交换链默认两块：0=后台画画，1=前台展示）
    // IID_PPV_ARGS：安全拿画布→避免拿错成其他东西（比如画笔）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    // 2. 给“后台画布”（空白白纸）涂“颜料吸附层”→生成“渲染目标视图”（带涂层的画布）
    // 第一个参数：要涂涂层的空白画布（pBackBuffer）
    // 第二个参数：nullptr→用默认涂层配方（和画布材质匹配，颜料不会掉）
    // 第三个参数：&g_mainRenderTargetView→把涂好层的画布存到全局变量，后续画画用
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);

    // 3. 把“空白白纸”（pBackBuffer）收起来→因为已经有“带涂层的画布”了，白纸没用了
    // 为什么要收？：画室空间有限，不用的东西要放回原位（避免内存泄漏）
    pBackBuffer->Release();
}

// ==============================================
// 【清理渲染目标视图 → 把“带涂层的画布”擦干净】
// 小白重点！！！
// 作用：换画布/关门时，把“带涂层的画布”上的颜料擦掉，避免下次画画有残留
// ==============================================
void CleanupRenderTarget()
{
    // 若“带涂层的画布”（g_mainRenderTargetView）存在→先擦干净（Release），再记为空（避免下次拿错）
    if (g_mainRenderTargetView) { 
        g_mainRenderTargetView->Release(); // 擦干净涂层和颜料
        g_mainRenderTargetView = nullptr;  // 标记“画布已清空”
    }
}

// ==============================================
// 【创建Direct3D设备和交换链 → 搭建“画室全套工具”】
// 小白重点！！！
// 核心概念类比：
// - Direct3D设备（g_pd3dDevice）= 颜料工厂：生产各种颜料（资源），比如红色、蓝色，还能制作画布涂层
// - Direct3D设备上下文（g_pd3dDeviceContext）= 画师的手：拿着颜料（设备生产的资源），在画布（渲染目标）上画画
// - 交换链（g_pSwapChain）= 双画布切换器+前台幕布：不仅有两块画布，还能把前台画布的内容显示到“画室窗户”（窗口hwnd）上，用户能看到
// 这一步就是：把颜料工厂、画师的手、双画布切换器都准备好，画室可以开工了
// ==============================================
bool CreateDeviceD3D(HWND hWnd)
{
    // 1. 给“双画布切换器”（交换链）写“配置单”→告诉工厂要做什么样的切换器
    DXGI_SWAP_CHAIN_DESC sd; // 配置单
    ZeroMemory(&sd, sizeof(sd)); // 先把配置单擦干净→避免之前的字迹干扰
    sd.BufferCount = 2;          // 要2块画布（双缓冲：1块后台画，1块前台显）
    sd.BufferDesc.Width = 0;     // 画布宽度：0=自动匹配“画室窗户”（窗口）大小，不用手动设
    sd.BufferDesc.Height = 0;    // 画布高度：同上，自动匹配窗口
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM; // 画布材质：能显示红（R）、绿（G）、蓝（B）、透明（A）四种颜色，和电脑屏幕匹配
    sd.BufferDesc.RefreshRate.Numerator = 60; // 切换画布的速度：每秒60次（避免画面闪）
    sd.BufferDesc.RefreshRate.Denominator = 1; 
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH; // 允许切换“显示模式”（比如窗口模式/全屏模式）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT; // 画布用途：专门用来画画（不是用来写字）
    sd.OutputWindow = hWnd;      // 把前台画布的内容显示到“哪个画室窗户”（窗口hwnd）
    sd.SampleDesc.Count = 1;     // 颜料细腻度：1=普通画质（够用，画得快），数字越大越细腻但越慢
    sd.SampleDesc.Quality = 0;   // 配合细腻度的参数，1对应0即可
    sd.Windowed = TRUE;          // 画布显示模式：TRUE=窗口模式（画布在窗户里），FALSE=全屏（画布占满整个屏幕）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD; // 切换画布后：后台画布的旧颜料扔掉（不用保存，下次重新画）

    // 2. 给“颜料工厂”（Direct3D设备）设“生产模式”
    UINT createDeviceFlags = 0;
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG; // 调试模式（开发时用，能提示哪里画错了，正式用要关掉）

    // 3. 告诉工厂“能生产哪些材质的颜料”（向下兼容旧电脑）
    D3D_FEATURE_LEVEL featureLevel; // 记录工厂实际能生产的最高级材质
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { 
        D3D_FEATURE_LEVEL_11_0, // 优先生产高级颜料（D3D11，新电脑支持）
        D3D_FEATURE_LEVEL_10_0  // 兼容旧电脑（D3D10，旧显卡也能画）
    };

    // 4. 核心步骤：按配置单“搭建全套工具”
    // D3D11CreateDeviceAndSwapChain：一站式创建4个东西：
    // - 颜料工厂（g_pd3dDevice）
    // - 画师的手（g_pd3dDeviceContext）
    // - 双画布切换器（g_pSwapChain）
    // - 记录工厂能生产的颜料材质（featureLevel）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );

    // 5. 兼容处理：若新电脑颜料工厂坏了（比如显卡不支持D3D11）→用“备用手工颜料”（WARP软件驱动，纯CPU画画，慢但能画）
    if (res == DXGI_ERROR_UNSUPPORTED) 
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );

    // 6. 若工具没搭好（res != S_OK）→画室开不了门，返回失败
    if (res != S_OK)
        return false;

    // 7. 最后一步：制作“能挂住颜料的画布”（调用前面的函数）→工具齐了，能画画了
    CreateRenderTarget();
    return true;
}

// ==============================================
// 【清理Direct3D资源 → 画室关门，收拾工具】
// 小白重点！！！
// 收拾顺序：先擦画布→再收切换器→再收手和工厂→避免工具损坏（资源泄漏）
// ==============================================
void CleanupDeviceD3D()
{
    CleanupRenderTarget(); // 1. 先擦干净“带涂层的画布”（避免颜料干在上面）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; } // 2. 收“双画布切换器”
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; } // 3. 收“画师的手”
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; } // 4. 关“颜料工厂”
}

// ==============================================
// 【程序入口 → 画室从开门到关门的全流程】
// 小白重点！！！关注“画画（渲染）”的完整步骤
// ==============================================
int main() {
    // -------------------------- 1. 调整画架大小 → 避免画布太小/模糊
    ImGui_ImplWin32_EnableDpiAwareness(); // 告诉画师“画室窗户（屏幕）的清晰度”→避免画的图模糊
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)
    ); // 算“缩放比例”→比如窗户是4K屏，比例=2.0，画架要放大2倍才清楚

    // -------------------------- 2. 租“画室窗户”（创建窗口）→ 用户能看到画布的地方
    WNDCLASSEXW wc = { sizeof(wc), CS_CLASSDC, WndProc, 0L, 0L, GetModuleHandle(nullptr), nullptr, nullptr, nullptr, nullptr, L"ImGui Example", nullptr };
    ::RegisterClassExW(&wc); // 告诉“画室管理员”要租窗户
    HWND hwnd = ::CreateWindowW(wc.lpszClassName, L"Dear ImGui DirectX11 Example", WS_OVERLAPPEDWINDOW, 100, 100, (int)(1280 * main_scale), (int)(800 * main_scale), nullptr, nullptr, wc.hInstance, nullptr); // 实际租到窗户

    // -------------------------- 3. 搭建画室工具 → 颜料工厂、手、切换器、画布
    if (!CreateDeviceD3D(hwnd))  // 若工具没搭好→关窗走人
    {
        CleanupDeviceD3D();      // 收拾已有的工具
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance); // 退租窗户
        return 1;
    }

    // -------------------------- 4. 打开窗户+请助理 → 准备接待用户
    ::ShowWindow(hwnd, SW_SHOWDEFAULT); // 打开窗户→用户能看到里面
    ::UpdateWindow(hwnd);               // 擦干净窗户→避免有灰尘（窗口空白）

    // 请“ImGUI助理”→负责画草图（UI）、记录用户需求
    IMGUI_CHECKVERSION();       // 检查助理资质→避免新手助理出错
    ImGui::CreateContext();     // 给助理安排工作间（上下文）
    ImGuiIO& io = ImGui::GetIO(); (void)io; // 给助理配“需求记录本”（IO对象）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;     // 助理要会看键盘需求（比如用户按Tab）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // 助理要会看手柄需求

    // 给助理说“画架缩放比例”→助理画的草图要和画架一样大
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);        // 草图里的按钮、文字→放大main_scale倍
    style.FontScaleDpi = main_scale;        // 草图里的字→也要放大，避免看不清

    // 助理和画师/工具对接→助理画的草图，画师能看懂
    ImGui_ImplWin32_Init(hwnd);            // 助理和窗户对接→知道草图要画在哪个窗户里
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext); // 助理和画师/工厂对接→知道用什么颜料画

    // -------------------------- 5. 准备画画的“素材”→ 要画的内容和背景色
    bool show_demo_window = true;   // 要不要画“示例草图”（比如按钮、滑块）
    bool show_another_window = false;// 要不要画“另一张草图”
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 画布背景色→蓝灰色（R=0.45, G=0.55, B=0.60, 透明=1.0）

    // -------------------------- 6. 画室日常运营（主循环）→ 持续画画、展示
    bool done = false; // 关门标志→false=开门，true=关门
    while (!done)
    {
        // 6.1 处理用户需求→助理记录，画师调整
        MSG msg;
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE)) // 看有没有新需求
        {
            ::TranslateMessage(&msg); // 助理翻译需求（比如用户按键盘→翻译成“要移动按钮”）
            ::DispatchMessage(&msg);  // 把需求传给画师（WndProc）
            if (msg.message == WM_QUIT) // 收到“关门”需求→标记要关门
                done = true;
        }
        if (done)
            break;

        // 6.2 检查用户是否在看→若窗户被挡住（用户看不到）→暂停画画
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10); // 休息10毫秒→节省颜料
            continue;
        }
        g_SwapChainOccluded = false;

        // 6.3 调整画架大小→用户之前说要改画架，现在动手
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)
        {
            CleanupRenderTarget(); // 先擦干净旧画布（避免颜料残留）
            // 调整“双画布切换器”的画布大小→和新画架匹配
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0; // 标记“已调整完”
            CreateRenderTarget(); // 重新做“带涂层的新画布”
        }

        // 6.4 助理准备画草图→告诉画师“今天要画什么”
        ImGui_ImplDX11_NewFrame(); // 助理告诉画师“颜料工厂准备好了”
        ImGui_ImplWin32_NewFrame(); // 助理告诉画师“窗户位置确认好了”
        ImGui::NewFrame();         // 助理开始画草图→比如画一个按钮、一段文字

        // （可选）助理画具体草图→比如画示例窗口、自定义按钮
        // if (show_demo_window)
        //     ImGui::ShowDemoWindow(&show_demo_window); // 画示例草图

        // ==============================================
        // 【渲染步骤 → 画师按草图在画布上画画！】
        // 小白重点！！！完整画画流程（渲染=按草图上颜料）
        // 1. 助理把草图交给画师（ImGui::Render()）→ 确定要画的内容和位置
        // 2. 画师调背景色→先把画布涂成背景色（避免有旧画）
        // 3. 画师把“带涂层的画布”固定在画架上→告诉自己“要画在这上面”
        // 4. 画师按草图上颜料→把按钮、文字画到画布上
        // 5. 切换画布→把后台画好的画布换到前台，用户看到新画
        // ==============================================
        // 1. 助理把草图（UI布局）整理好交给画师→生成“画画指令”（比如“在(100,100)画红色按钮”）
        ImGui::Render();

        // 2. 画师调背景色→把“蓝灰色”颜料按比例调好（乘透明度，避免太浓）
        const float clear_color_with_alpha[4] = { 
            clear_color.x * clear_color.w, // 红色分量（乘透明度）
            clear_color.y * clear_color.w, // 绿色分量
            clear_color.z * clear_color.w, // 蓝色分量
            clear_color.w                  // 透明度
        };

        // 3. 画师把“带涂层的画布”（g_mainRenderTargetView）固定在“画架”（设备上下文）上
        // OMSetRenderTargets：告诉画师“接下来要画在这块画布上，别画错了”
        // 第一个参数：1→只固定1块画布
        // 第二个参数：&g_mainRenderTargetView→要固定的画布（带涂层的后台画布）
        // 第三个参数：nullptr→不用画景深（简单场景不用）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);

        // 4. 画师先给画布涂背景色→用调好的蓝灰色把画布整个涂一遍，覆盖旧画
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);

        // 5. 画师按“画画指令”（ImGui::GetDrawData()）在画布上画具体内容→比如按钮、文字
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // 6. 切换画布→把“后台画好的画布”（带新画）和“前台展示的画布”快速交换
        // Present(1, 0)：1→每秒只换60次（和屏幕刷新同步，避免画面闪），0→无额外设置
        HRESULT hr = g_pSwapChain->Present(1, 0);   
        // 检查窗户是否被挡住→更新标志，下次挡住就暂停画画
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 7. 画室关门→收拾所有东西
    // 先让助理下班→清理助理的工作间和记录本
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();

    // 再收拾画师工具→擦画布、收切换器、关工厂
    CleanupDeviceD3D();

    // 最后退租窗户→把窗户还给管理员
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

	return 0; // 画室成功关门，返回0表示一切正常
}

```

## 3. 3.ImGui-窗体

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151080311
- Description: æç« æµè§éè¯»867æ¬¡ï¼ç¹èµ8æ¬¡ï¼æ¶è3æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_imgui input æ§ä»¶ æ æ³è¾å¥ä¸­æ

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：2.ImGui-搭建一个外部绘制的窗口环境（使用ImGui绘制一个空白窗口） 
创建我们的窗体，如下图红框通过两行代码创建的窗体，然后可以发现它中文是?，这个原因是我们没有导入字体，或者说IMGui默认的字体库不支持中文，需要我自己手动导入一个支持中文的字体库(后面会导入) 
 
鼠标拖动下图红框位置，可以改变窗体的大小 
 
然后点击下图红框停止运行 
 
然后点击下图红框再次运行 
 
会发现我们创建的窗体，它会保持上一次我们修改过的大小和位置，这是因为它有一个文件在保存这些数据 
 
配置文件位置，首先点击打开所在的文件夹 
 
如果是通过vs运行的它的配置文件在下图红框位置 imgui.ini 
 
它的内容，pos是坐标x和y，size是大小 
 
如果是通过双击下图红框的exe文件运行的程序 
 
它就会在双击运行的exe目录下创建 imgui.ini文件 
 
第三个参数的值，下方的代码都是从ImGui的原理复制出来的

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：2.ImGui-搭建一个外部绘制的窗口环境（使用ImGui绘制一个空白窗口） 
创建我们的窗体，如下图红框通过两行代码创建的窗体，然后可以发现它中文是?，这个原因是我们没有导入字体，或者说IMGui默认的字体库不支持中文，需要我自己手动导入一个支持中文的字体库(后面会导入) 
 
鼠标拖动下图红框位置，可以改变窗体的大小 
 
然后点击下图红框停止运行 
 
然后点击下图红框再次运行 
 
会发现我们创建的窗体，它会保持上一次我们修改过的大小和位置，这是因为它有一个文件在保存这些数据 
 
配置文件位置，首先点击打开所在的文件夹 
 
如果是通过vs运行的它的配置文件在下图红框位置 imgui.ini 
 
它的内容，pos是坐标x和y，size是大小 
 
如果是通过双击下图红框的exe文件运行的程序 
 
它就会在双击运行的exe目录下创建 imgui.ini文件 
 
第三个参数的值，下方的代码都是从ImGui的原理复制出来的 

```text
// ImGui 窗口标志枚举（用于控制窗口的各种行为和样式）
enum ImGuiWindowFlags_
{
    ImGuiWindowFlags_None                   = 0,  // 无任何特殊设置（默认状态）
    ImGuiWindowFlags_NoTitleBar             = 1 << 0,   // 禁用窗口的标题栏
    ImGuiWindowFlags_NoResize               = 1 << 1,   // 禁用用户通过右下角调整窗口大小的功能
    ImGuiWindowFlags_NoMove                 = 1 << 2,   // 禁用用户拖动窗口改变位置的功能
    ImGuiWindowFlags_NoScrollbar            = 1 << 3,   // 禁用滚动条（窗口仍可通过鼠标或代码控制滚动）
    ImGuiWindowFlags_NoScrollWithMouse      = 1 << 4,   // 禁用鼠标滚轮控制窗口垂直滚动。如果是子窗口，鼠标滚轮事件可能会传递给父窗口（除非同时设置了NoScrollbar）
    ImGuiWindowFlags_NoCollapse             = 1 << 5,   // 禁用用户通过双击窗口折叠窗口的功能（也会影响窗口菜单按钮，比如在 docking 布局中的按钮）
    ImGuiWindowFlags_AlwaysAutoResize       = 1 << 6,   // 窗口会在每一帧自动调整大小，以适应其内容
    ImGuiWindowFlags_NoBackground           = 1 << 7,   // 禁用绘制窗口背景色（WindowBg等）和外边框，效果类似调用SetNextWindowBgAlpha(0.0f)（设置背景透明度为0）
    ImGuiWindowFlags_NoSavedSettings        = 1 << 8,   // 从不将窗口的设置（位置、大小等）保存到.ini文件，也不从.ini文件加载这些设置
    ImGuiWindowFlags_NoMouseInputs          = 1 << 9,   // 禁用窗口捕获鼠标输入，鼠标悬停会"穿透"到窗口下方（不响应任何鼠标事件）
    ImGuiWindowFlags_MenuBar                = 1 << 10,  // 窗口包含菜单栏
    ImGuiWindowFlags_HorizontalScrollbar    = 1 << 11,  // 允许水平滚动条出现（默认关闭）。可在调用Begin()前用SetNextWindowContentSize(ImVec2(width,0.0f))指定宽度，参考imgui_demo中的"Horizontal Scrolling"示例
    ImGuiWindowFlags_NoFocusOnAppearing     = 1 << 12,  // 当窗口从隐藏状态变为可见状态时，不自动获取焦点
    ImGuiWindowFlags_NoBringToFrontOnFocus  = 1 << 13,  // 当窗口获取焦点时（比如点击窗口或通过代码设置焦点），不将窗口提到最前面
    ImGuiWindowFlags_AlwaysVerticalScrollbar= 1 << 14,  // 总是显示垂直滚动条（即使内容高度小于窗口高度）
    ImGuiWindowFlags_AlwaysHorizontalScrollbar=1<< 15,  // 总是显示水平滚动条（即使内容宽度小于窗口宽度）
    ImGuiWindowFlags_NoNavInputs            = 1 << 16,  // 禁用窗口内的键盘/手柄导航功能（无法用键盘/手柄操作窗口内容）
    ImGuiWindowFlags_NoNavFocus             = 1 << 17,  // 通过键盘/手柄导航时，不能聚焦到这个窗口（比如会被CTRL+TAB等导航方式跳过）
    ImGuiWindowFlags_UnsavedDocument        = 1 << 18,  // 在窗口标题旁显示一个小点（表示有未保存的内容）。在标签页或docking场景中：点击关闭按钮时不会立即关闭标签（会等用户停止提交该标签）；否则点击X会关闭窗口，若继续提交该窗口可能重新出现在标签栏末尾
    ImGuiWindowFlags_NoNav                  = ImGuiWindowFlags_NoNavInputs | ImGuiWindowFlags_NoNavFocus,  // 组合标志：同时禁用导航输入和导航聚焦（等于上面两个标志的组合）
    ImGuiWindowFlags_NoDecoration           = ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoScrollbar | ImGuiWindowFlags_NoCollapse,  // 组合标志：同时禁用标题栏、调整大小、滚动条和折叠功能（上面四个标志的组合）
    ImGuiWindowFlags_NoInputs               = ImGuiWindowFlags_NoMouseInputs | ImGuiWindowFlags_NoNavInputs | ImGuiWindowFlags_NoNavFocus,  // 组合标志：同时禁用鼠标输入、导航输入和导航聚焦（上面三个标志的组合）

    // 【内部使用】以下标志由ImGui内部函数使用，不建议手动设置
    ImGuiWindowFlags_ChildWindow            = 1 << 24,  // 不要手动使用！供BeginChild()函数内部使用（子窗口专用）
    ImGuiWindowFlags_Tooltip                = 1 << 25,  // 不要手动使用！供BeginTooltip()函数内部使用（提示框专用）
    ImGuiWindowFlags_Popup                  = 1 << 26,  // 不要手动使用！供BeginPopup()函数内部使用（弹窗专用）
    ImGuiWindowFlags_Modal                  = 1 << 27,  // 不要手动使用！供BeginPopupModal()函数内部使用（模态弹窗专用）
    ImGuiWindowFlags_ChildMenu              = 1 << 28,  // 不要手动使用！供BeginMenu()函数内部使用（子菜单专用）

    // 过时的标志（旧版本使用，新版本已废弃）
#ifndef IMGUI_DISABLE_OBSOLETE_FUNCTIONS
    ImGuiWindowFlags_NavFlattened           = 1 << 29,  // 在1.90.9版本后废弃：请在BeginChild()中使用ImGuiChildFlags_NavFlattened
    ImGuiWindowFlags_AlwaysUseWindowPadding = 1 << 30,  // 在1.90.0版本后废弃：请在BeginChild()中使用ImGuiChildFlags_AlwaysUseWindowPadding
#endif
};

```
 
 
使用这些样式 
 
完整代码： 

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 窗口消息处理函数：处理所有窗口事件（如点击、关闭、调整大小等）
// 参数：
// - hWnd：窗口句柄（标识当前窗口）
// - msg：消息类型（如WM_SIZE表示窗口大小改变）
// - wParam：消息附加参数（如WM_SIZE中表示 resize 类型）
// - lParam：消息附加参数（如WM_SIZE中存储新的宽高）
// 返回值：LRESULT类型（消息处理结果，0表示成功处理）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是ImGui的UI控件触发的事件，优先由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;  // ImGui已处理，直接返回

    // 根据消息类型处理不同事件
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        if (wParam == SIZE_MINIMIZED)  // 如果是窗口最小化，无需处理渲染相关
            return 0;
        // 从lParam中提取新的窗口尺寸：低16位是宽度，高16位是高度
        g_ResizeWidth = (UINT)LOWORD(lParam);  // 记录新宽度
        g_ResizeHeight = (UINT)HIWORD(lParam); // 记录新高度
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单（避免菜单遮挡ImGui控件，影响操作体验）
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标（ImGui绘制的内容会输出到这里）
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时存储交换链的后台缓冲区

    // 从交换链获取后台缓冲区（参数0表示第一个缓冲区，IID_ID3D11Texture2D指定缓冲区类型）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    // 用D3D设备创建渲染目标视图（将后台缓冲区转换为可渲染的目标）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    // 释放临时缓冲区（渲染目标视图已引用它，无需保留此指针）
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
void CleanupRenderTarget()
{
    // 释放渲染目标视图（COM对象需调用Release()减少引用计数，为0时自动释放内存）
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：hWnd - 窗口句柄（渲染结果会显示在这个窗口）
// 返回值：bool - 成功创建返回true，失败返回false
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述（定义交换链的属性，告诉系统如何创建交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值导致错误
    sd.BufferCount = 2;           // 缓冲区数量（2=双缓冲，避免画面闪烁）
    sd.BufferDesc.Width = 0;      // 缓冲区宽度（0=自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;     // 缓冲区高度（0=自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位色，含透明度）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60=60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;       // 绑定的窗口（渲染结果显示到该窗口）
    sd.SampleDesc.Count = 1;      // 多重采样数量（1=无抗锯齿，性能优先）
    sd.SampleDesc.Quality = 0;    // 采样质量（0=默认）
    sd.Windowed = TRUE;           // 窗口模式（TRUE=窗口，FALSE=全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台数据，性能最好）

    UINT createDeviceFlags = 0;   // 创建设备的标志（0=默认，调试时可加D3D11_CREATE_DEVICE_DEBUG）
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 调试模式（需安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的D3D版本（如11.0、10.0）
    // 支持的D3D版本列表（优先11.0，不支持则用10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };

    // 创建设备、设备上下文和交换链（DirectX核心函数）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE,  // 使用硬件加速（显卡渲染）
        nullptr, createDeviceFlags,         // 无软件渲染模块，创建标志
        featureLevelArray, 2,               // 支持的D3D版本列表及数量
        D3D11_SDK_VERSION, &sd,             // SDK版本，交换链描述
        &g_pSwapChain, &g_pd3dDevice,       // 输出交换链和设备
        &featureLevel, &g_pd3dDeviceContext // 输出支持的版本和设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,   // 软件渲染（性能较差，兼容旧设备）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象，避免内存泄漏
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标

    // 释放COM对象（按依赖顺序释放，避免资源冲突）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

// 主函数：程序入口，控制整个程序的生命周期
int main() {
    // -------------------------- 步骤1：DPI适配（解决高分辨率屏幕UI模糊问题） --------------------------
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知
    // 获取主显示器的DPI缩放比例（如4K屏幕可能为2.0，1080P可能为1.0）
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)  // 获取主显示器
    );

    // -------------------------- 步骤2：创建Windows窗口（ImGui需要依附的窗口载体） --------------------------
    // 定义窗口类（描述窗口的基本属性，如消息处理函数、图标等）
    WNDCLASSEXW wc = { 
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格（使用专属设备上下文，避免绘图冲突）
        WndProc,                     // 消息处理函数
        0L, 0L,                      // 额外数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景等（用默认）
        L"ImGui Example",            // 窗口类名（自定义，后续创建窗口需使用）
        nullptr                      // 小图标（默认）
    };
    ::RegisterClassExW(&wc);  // 注册窗口类（向系统注册这个窗口类型）

    // 创建窗口（生成实际窗口）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名（对应注册的类）
        L"Dear ImGui DirectX11 Example",  // 窗口标题
        WS_OVERLAPPEDWINDOW,         // 窗口风格（标准窗口，带标题栏、关闭按钮等）
        100, 100,                    // 初始位置（屏幕左上角x=100，y=100）
        (int)(1280 * main_scale),    // 宽度（1280 * DPI缩放，适配高分辨率）
        (int)(800 * main_scale),     // 高度（800 * DPI缩放）
        nullptr, nullptr,            // 父窗口、菜单（无）
        wc.hInstance, nullptr        // 程序实例、额外参数
    );

    // -------------------------- 步骤3：初始化DirectX 11（创建渲染环境） --------------------------
    if (!CreateDeviceD3D(hwnd))  // 调用函数创建D3D设备和交换链，失败则清理资源并退出
    {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后默认隐藏，需手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保立即显示

    // -------------------------- 步骤4：初始化ImGui（配置UI环境） --------------------------
    IMGUI_CHECKVERSION();  // 检查ImGui版本（确保编译版本与运行时一致）
    ImGui::CreateContext(); // 创建ImGui上下文（UI的"全局环境"）
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象（管理输入输出，如键盘、帧率）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab操作UI）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启手柄导航（支持游戏手柄操作）

    // -------------------------- 步骤5：设置UI缩放（适配DPI，避免高分辨率下UI过小） --------------------------
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素（按钮、文本等）
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // -------------------------- 步骤6：初始化ImGui后端（连接ImGui与系统/渲染API） --------------------------
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端（处理窗口消息、输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端（负责渲染UI）

    // -------------------------- 步骤7：程序状态变量（控制UI显示） --------------------------
    bool show_demo_window = true;    // 是否显示ImGui演示窗口
    bool show_another_window = false; // 是否显示"另一个窗口"
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）

    // -------------------------- 步骤8：主循环（程序的核心，持续运行直到退出） --------------------------
    bool done = false;  // 控制循环是否结束（true=退出）
    while (!done)
    {
        // -------------------------- 8.1 处理窗口消息（如关闭、点击等） --------------------------
        MSG msg;  // 存储消息的结构体
        // 从消息队列中获取消息（PM_REMOVE表示获取后移除，避免重复处理）
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如键盘按键转字符）
            ::DispatchMessage(&msg);   // 分发消息到WndProc处理
            if (msg.message == WM_QUIT)  // 收到退出消息（如点击关闭按钮）
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出循环

        // -------------------------- 8.2 处理窗口遮挡（优化性能） --------------------------
        // 如果交换链被遮挡（如窗口被覆盖），且确认遮挡状态：
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10ms，减少CPU占用
            continue;     // 跳过本次循环，不渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // -------------------------- 8.3 处理窗口大小调整（避免画面拉伸） --------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)  // 如果有新的窗口尺寸
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标
            // 调整交换链缓冲区大小（匹配新窗口尺寸）
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标（适配新尺寸）
        }

        // -------------------------- 8.4 开始ImGui新帧（准备绘制UI） --------------------------
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧
        ImGui::NewFrame();          // ImGui核心准备（通知ImGui可以开始定义UI了）

        // -------------------------- 8.5 定义UI界面（核心：这里是你要显示的UI） --------------------------
        /**
            ImGui::Begin()函数说明：
            函数声明：bool Begin(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0);
            参数：
            - name：窗口标题（唯一标识，相同标题会合并窗口）
            - p_open：控制窗口是否显示的指针（关闭窗口时会将其设为false）
            - flags：窗口标志（组合使用，如禁用标题栏、禁止移动等）
        */
        bool i = true;  // 控制窗口是否显示（true=显示）
        // 创建一个自定义窗口：标题为"我的IMGui"，禁止标题栏（NoTitleBar）和移动（NoMove）
        ImGui::Begin("我的IMGui", &i, ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoMove);

        // 这里可以添加其他UI控件（如按钮、文本等），目前是空窗口
        // 例如：ImGui::Text("这是我的第一个ImGui窗口！");

        ImGui::End();  // 结束窗口定义（必须与Begin配对，否则崩溃）

        // -------------------------- 8.6 渲染UI（将定义的UI绘制到屏幕） --------------------------
        ImGui::Render();  // 生成绘制命令（将UI转换为显卡可执行的指令）

        // 计算背景色（考虑透明度：clear_color.w是透明度，乘以RGB值）
        const float clear_color_with_alpha[4] = { 
            clear_color.x * clear_color.w, 
            clear_color.y * clear_color.w, 
            clear_color.z * clear_color.w, 
            clear_color.w 
        };

        // 设置渲染目标（告诉显卡：接下来的绘制输出到主渲染目标）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空屏幕（用背景色填充，避免上一帧画面残留）
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        // 渲染ImGui的UI（执行绘制命令，将UI画到屏幕）
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // -------------------------- 8.7 显示画面（交换前后缓冲区，展示渲染结果） --------------------------
        // Present函数：交换前后缓冲区（后台缓冲区是刚渲染的画面，前台是正在显示的）
        // 参数1：1=开启垂直同步（VSync，防止画面撕裂，帧率与显示器一致）；0=关闭（帧率更高）
        HRESULT hr = g_pSwapChain->Present(1, 0);   // 开启垂直同步
        // HRESULT hr = g_pSwapChain->Present(0, 0); // 关闭垂直同步

        // 检查交换链是否被遮挡（用于后续优化）
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 步骤9：程序退出，清理资源 --------------------------
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 4. 4.ImGui-静态文本框

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151119400
- Description: æç« æµè§éè¯»647æ¬¡ï¼ç¹èµ6æ¬¡ï¼æ¶è5æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui::begin

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：3.ImGui-窗体 
样式如下图红框，下图是ImGui源码的实例，接下来就实现它 
 
窗口中的内容（代码）要写在下图红框的Begin后面End前面，也就是写在Begin和End之间 
 
在ImGui源码中搜索文字找它的代码，如下图红框 
 
点击查询全部后就会出现下图红框，然后鼠标左键双击它 
 
然后就找到了它的代码，如下图红框，然后把下图红框的代码复制到我们的代码中 
 
如下图复制到我们的代码中后然后运行就可以看到我们的窗口也有了文本内容 
 
如下图红框在源码附近也可以看到其它的静态文本框的实现，想要那个直接复制到自己的代码中就可以了 
 
如下图红框带颜色的文本和在同一行显示的文本 
 
鼠标放到下图红框位置，它会显示下图蓝框的内容，下图蓝框的叫做悬浮文本框 
 
这个是由下图红框的代码实现 
 
把它复制到我们代码中会报错，还是接着复制 
 
把下图红框的代码全复制到我们的代码 
 
如下图红框，复制过来就不报错了 
 
然后我们也有了这个东西 
 
完整代码

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：3.ImGui-窗体 
样式如下图红框，下图是ImGui源码的实例，接下来就实现它 
 
窗口中的内容（代码）要写在下图红框的Begin后面End前面，也就是写在Begin和End之间 
 
在ImGui源码中搜索文字找它的代码，如下图红框 
 
点击查询全部后就会出现下图红框，然后鼠标左键双击它 
 
然后就找到了它的代码，如下图红框，然后把下图红框的代码复制到我们的代码中 
 
如下图复制到我们的代码中后然后运行就可以看到我们的窗口也有了文本内容 
 
如下图红框在源码附近也可以看到其它的静态文本框的实现，想要那个直接复制到自己的代码中就可以了 
 
如下图红框带颜色的文本和在同一行显示的文本 
 
鼠标放到下图红框位置，它会显示下图蓝框的内容，下图蓝框的叫做悬浮文本框 
 
这个是由下图红框的代码实现 
 
把它复制到我们代码中会报错，还是接着复制 
 
把下图红框的代码全复制到我们的代码 
 
如下图红框，复制过来就不报错了 
 
然后我们也有了这个东西 
 
完整代码 

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

// 窗口消息处理函数：处理所有窗口事件（如点击、关闭、调整大小等）
// 参数：
// - hWnd：窗口句柄（标识当前窗口）
// - msg：消息类型（如WM_SIZE表示窗口大小改变）
// - wParam：消息附加参数（如WM_SIZE中表示 resize 类型）
// - lParam：消息附加参数（如WM_SIZE中存储新的宽高）
// 返回值：LRESULT类型（消息处理结果，0表示成功处理）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是ImGui的UI控件触发的事件，优先由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;  // ImGui已处理，直接返回

    // 根据消息类型处理不同事件
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        if (wParam == SIZE_MINIMIZED)  // 如果是窗口最小化，无需处理渲染相关
            return 0;
        // 从lParam中提取新的窗口尺寸：低16位是宽度，高16位是高度
        g_ResizeWidth = (UINT)LOWORD(lParam);  // 记录新宽度
        g_ResizeHeight = (UINT)HIWORD(lParam); // 记录新高度
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单（避免菜单遮挡ImGui控件，影响操作体验）
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标（ImGui绘制的内容会输出到这里）
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时存储交换链的后台缓冲区

    // 从交换链获取后台缓冲区（参数0表示第一个缓冲区，IID_ID3D11Texture2D指定缓冲区类型）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    // 用D3D设备创建渲染目标视图（将后台缓冲区转换为可渲染的目标）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    // 释放临时缓冲区（渲染目标视图已引用它，无需保留此指针）
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
void CleanupRenderTarget()
{
    // 释放渲染目标视图（COM对象需调用Release()减少引用计数，为0时自动释放内存）
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：hWnd - 窗口句柄（渲染结果会显示在这个窗口）
// 返回值：bool - 成功创建返回true，失败返回false
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述（定义交换链的属性，告诉系统如何创建交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值导致错误
    sd.BufferCount = 2;           // 缓冲区数量（2=双缓冲，避免画面闪烁）
    sd.BufferDesc.Width = 0;      // 缓冲区宽度（0=自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;     // 缓冲区高度（0=自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位色，含透明度）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60=60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;       // 绑定的窗口（渲染结果显示到该窗口）
    sd.SampleDesc.Count = 1;      // 多重采样数量（1=无抗锯齿，性能优先）
    sd.SampleDesc.Quality = 0;    // 采样质量（0=默认）
    sd.Windowed = TRUE;           // 窗口模式（TRUE=窗口，FALSE=全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台数据，性能最好）

    UINT createDeviceFlags = 0;   // 创建设备的标志（0=默认，调试时可加D3D11_CREATE_DEVICE_DEBUG）
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 调试模式（需安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的D3D版本（如11.0、10.0）
    // 支持的D3D版本列表（优先11.0，不支持则用10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };

    // 创建设备、设备上下文和交换链（DirectX核心函数）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE,  // 使用硬件加速（显卡渲染）
        nullptr, createDeviceFlags,         // 无软件渲染模块，创建标志
        featureLevelArray, 2,               // 支持的D3D版本列表及数量
        D3D11_SDK_VERSION, &sd,             // SDK版本，交换链描述
        &g_pSwapChain, &g_pd3dDevice,       // 输出交换链和设备
        &featureLevel, &g_pd3dDeviceContext // 输出支持的版本和设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,   // 软件渲染（性能较差，兼容旧设备）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象，避免内存泄漏
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标

    // 释放COM对象（按依赖顺序释放，避免资源冲突）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

// 主函数：程序入口，控制整个程序的生命周期
int main() {
    // -------------------------- 步骤1：DPI适配（解决高分辨率屏幕UI模糊问题） --------------------------
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知
    // 获取主显示器的DPI缩放比例（如4K屏幕可能为2.0，1080P可能为1.0）
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)  // 获取主显示器
    );

    // -------------------------- 步骤2：创建Windows窗口（ImGui需要依附的窗口载体） --------------------------
    // 定义窗口类（描述窗口的基本属性，如消息处理函数、图标等）
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格（使用专属设备上下文，避免绘图冲突）
        WndProc,                     // 消息处理函数
        0L, 0L,                      // 额外数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景等（用默认）
        L"ImGui Example",            // 窗口类名（自定义，后续创建窗口需使用）
        nullptr                      // 小图标（默认）
    };
    ::RegisterClassExW(&wc);  // 注册窗口类（向系统注册这个窗口类型）

    // 创建窗口（生成实际窗口）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名（对应注册的类）
        L"Dear ImGui DirectX11 Example",  // 窗口标题
        WS_OVERLAPPEDWINDOW,         // 窗口风格（标准窗口，带标题栏、关闭按钮等）
        100, 100,                    // 初始位置（屏幕左上角x=100，y=100）
        (int)(1280 * main_scale),    // 宽度（1280 * DPI缩放，适配高分辨率）
        (int)(800 * main_scale),     // 高度（800 * DPI缩放）
        nullptr, nullptr,            // 父窗口、菜单（无）
        wc.hInstance, nullptr        // 程序实例、额外参数
    );

    // -------------------------- 步骤3：初始化DirectX 11（创建渲染环境） --------------------------
    if (!CreateDeviceD3D(hwnd))  // 调用函数创建D3D设备和交换链，失败则清理资源并退出
    {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后默认隐藏，需手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保立即显示

    // -------------------------- 步骤4：初始化ImGui（配置UI环境） --------------------------
    IMGUI_CHECKVERSION();  // 检查ImGui版本（确保编译版本与运行时一致）
    ImGui::CreateContext(); // 创建ImGui上下文（UI的"全局环境"）
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象（管理输入输出，如键盘、帧率）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab操作UI）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启手柄导航（支持游戏手柄操作）

    // -------------------------- 步骤5：设置UI缩放（适配DPI，避免高分辨率下UI过小） --------------------------
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素（按钮、文本等）
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // -------------------------- 步骤6：初始化ImGui后端（连接ImGui与系统/渲染API） --------------------------
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端（处理窗口消息、输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端（负责渲染UI）

    // -------------------------- 步骤7：程序状态变量（控制UI显示） --------------------------
    bool show_demo_window = true;    // 是否显示ImGui演示窗口
    bool show_another_window = false; // 是否显示"另一个窗口"
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）

    // -------------------------- 步骤8：主循环（程序的核心，持续运行直到退出） --------------------------
    bool done = false;  // 控制循环是否结束（true=退出）
    while (!done)
    {
        // -------------------------- 8.1 处理窗口消息（如关闭、点击等） --------------------------
        MSG msg;  // 存储消息的结构体
        // 从消息队列中获取消息（PM_REMOVE表示获取后移除，避免重复处理）
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如键盘按键转字符）
            ::DispatchMessage(&msg);   // 分发消息到WndProc处理
            if (msg.message == WM_QUIT)  // 收到退出消息（如点击关闭按钮）
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出循环

        // -------------------------- 8.2 处理窗口遮挡（优化性能） --------------------------
        // 如果交换链被遮挡（如窗口被覆盖），且确认遮挡状态：
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10ms，减少CPU占用
            continue;     // 跳过本次循环，不渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // -------------------------- 8.3 处理窗口大小调整（避免画面拉伸） --------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)  // 如果有新的窗口尺寸
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标
            // 调整交换链缓冲区大小（匹配新窗口尺寸）
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标（适配新尺寸）
        }

        // -------------------------- 8.4 开始ImGui新帧（准备绘制UI） --------------------------
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧
        ImGui::NewFrame();          // ImGui核心准备（通知ImGui可以开始定义UI了）

        // -------------------------- 8.5 定义UI界面（核心：这里是你要显示的UI） --------------------------
        /**
            ImGui::Begin()函数说明：
            函数声明：bool Begin(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0);
            参数：
            - name：窗口标题（唯一标识，相同标题会合并窗口）
            - p_open：控制窗口是否显示的指针（关闭窗口时会将其设为false）
            - flags：窗口标志（组合使用，如禁用标题栏、禁止移动等）
        */
        bool i = true;  // 控制窗口是否显示（true=显示）
        // 创建一个自定义窗口：标题为"我的IMGui"，禁止标题栏（NoTitleBar）和移动（NoMove）
        ImGui::Begin("我的IMGui", &i);

        // 这里可以添加其他UI控件（如按钮、文本等），目前是空窗口
        // 例如：ImGui::Text("这是我的第一个ImGui窗口！");
        // 长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");

        // 带颜色的文本框
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        // 鼠标悬浮上去会显示悬浮文本框，悬浮文本框会显示52am
        HelpMarker("52am");

        ImGui::End();  // 结束窗口定义（必须与Begin配对，否则崩溃）

        // -------------------------- 8.6 渲染UI（将定义的UI绘制到屏幕） --------------------------
        ImGui::Render();  // 生成绘制命令（将UI转换为显卡可执行的指令）

        // 计算背景色（考虑透明度：clear_color.w是透明度，乘以RGB值）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标（告诉显卡：接下来的绘制输出到主渲染目标）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空屏幕（用背景色填充，避免上一帧画面残留）
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        // 渲染ImGui的UI（执行绘制命令，将UI画到屏幕）
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // -------------------------- 8.7 显示画面（交换前后缓冲区，展示渲染结果） --------------------------
        // Present函数：交换前后缓冲区（后台缓冲区是刚渲染的画面，前台是正在显示的）
        // 参数1：1=开启垂直同步（VSync，防止画面撕裂，帧率与显示器一致）；0=关闭（帧率更高）
        HRESULT hr = g_pSwapChain->Present(1, 0);   // 开启垂直同步
        // HRESULT hr = g_pSwapChain->Present(0, 0); // 关闭垂直同步

        // 检查交换链是否被遮挡（用于后续优化）
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 步骤9：程序退出，清理资源 --------------------------
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 5. 5.ImGui-按钮

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151155233
- Description: æç« æµè§éè¯»868æ¬¡ï¼ç¹èµ13æ¬¡ï¼æ¶è5æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui rgbè²å¡

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：4.ImGui-静态文本框 
按钮的代码

```text
ImGui::Button("anNiu")

```
 
 
修改按钮的颜色，鼠标放上去的颜色，鼠标点击的颜色，鼠标未放上去的颜色

```text
  // ImGui中通过PushStyleColor()临时修改按钮在不同状态下的颜色
  // 注意：每次PushStyleColor()后必须用PopStyleColor()恢复默认样式，否则会影响后续UI元素

// 1. 修改按钮"正常状态"（未被鼠标悬停、未被点击）的背景色
  // 参数1：ImGuiCol_Button - 指定修改"按钮正常状态"的颜色
  // 参数2：{1.0f, 1.0f, 0.0f, 1.0f} - RGBA颜色值（每个分量范围0.0f~1.0f）
  //   R=1.0f（红色满值）、G=1.0f（绿色满值）、B=0.0f（蓝色无）→ 混合为黄色
  //   A=1.0f（透明度100%，完全不透明）
  ImGui::PushStyleColor(ImGuiCol_Button, { 1.0f,1.0f,0.0f, 1.0f });

// 2. 修改按钮"鼠标悬停状态"（鼠标放在按钮上但未点击）的背景色
  // 参数1：ImGuiCol_ButtonHovered - 指定修改"按钮被悬停时"的颜色
  // 参数2：{1.0f, 0.0f, 0.0f, 1.0f} → 红色（R满值，G、B无），完全不透明
  ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f, 1.0f });

// 3. 修改按钮"激活状态"（鼠标按下按钮但未松开）的背景色
  // 参数1：ImGuiCol_ButtonActive - 指定修改"按钮被点击时"的颜色
  // 参数2：{0.0f, 1.0f, 0.0f, 1.0f} → 绿色（G满值，R、B无），完全不透明
  ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f, 1.0f });

```
 
 
完整代码

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：4.ImGui-静态文本框 
按钮的代码 

```text
ImGui::Button("anNiu")

```
 
 
修改按钮的颜色，鼠标放上去的颜色，鼠标点击的颜色，鼠标未放上去的颜色 

```text
  // ImGui中通过PushStyleColor()临时修改按钮在不同状态下的颜色
  // 注意：每次PushStyleColor()后必须用PopStyleColor()恢复默认样式，否则会影响后续UI元素

  // 1. 修改按钮"正常状态"（未被鼠标悬停、未被点击）的背景色
  // 参数1：ImGuiCol_Button - 指定修改"按钮正常状态"的颜色
  // 参数2：{1.0f, 1.0f, 0.0f, 1.0f} - RGBA颜色值（每个分量范围0.0f~1.0f）
  //   R=1.0f（红色满值）、G=1.0f（绿色满值）、B=0.0f（蓝色无）→ 混合为黄色
  //   A=1.0f（透明度100%，完全不透明）
  ImGui::PushStyleColor(ImGuiCol_Button, { 1.0f,1.0f,0.0f, 1.0f });

  // 2. 修改按钮"鼠标悬停状态"（鼠标放在按钮上但未点击）的背景色
  // 参数1：ImGuiCol_ButtonHovered - 指定修改"按钮被悬停时"的颜色
  // 参数2：{1.0f, 0.0f, 0.0f, 1.0f} → 红色（R满值，G、B无），完全不透明
  ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f, 1.0f });

  // 3. 修改按钮"激活状态"（鼠标按下按钮但未松开）的背景色
  // 参数1：ImGuiCol_ButtonActive - 指定修改"按钮被点击时"的颜色
  // 参数2：{0.0f, 1.0f, 0.0f, 1.0f} → 绿色（G满值，R、B无），完全不透明
  ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f, 1.0f });

```
 
 
完整代码 

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

// 窗口消息处理函数：处理所有窗口事件（如点击、关闭、调整大小等）
// 参数：
// - hWnd：窗口句柄（标识当前窗口）
// - msg：消息类型（如WM_SIZE表示窗口大小改变）
// - wParam：消息附加参数（如WM_SIZE中表示 resize 类型）
// - lParam：消息附加参数（如WM_SIZE中存储新的宽高）
// 返回值：LRESULT类型（消息处理结果，0表示成功处理）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是ImGui的UI控件触发的事件，优先由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;  // ImGui已处理，直接返回

    // 根据消息类型处理不同事件
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        if (wParam == SIZE_MINIMIZED)  // 如果是窗口最小化，无需处理渲染相关
            return 0;
        // 从lParam中提取新的窗口尺寸：低16位是宽度，高16位是高度
        g_ResizeWidth = (UINT)LOWORD(lParam);  // 记录新宽度
        g_ResizeHeight = (UINT)HIWORD(lParam); // 记录新高度
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单（避免菜单遮挡ImGui控件，影响操作体验）
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标（ImGui绘制的内容会输出到这里）
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时存储交换链的后台缓冲区

    // 从交换链获取后台缓冲区（参数0表示第一个缓冲区，IID_ID3D11Texture2D指定缓冲区类型）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    // 用D3D设备创建渲染目标视图（将后台缓冲区转换为可渲染的目标）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    // 释放临时缓冲区（渲染目标视图已引用它，无需保留此指针）
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
void CleanupRenderTarget()
{
    // 释放渲染目标视图（COM对象需调用Release()减少引用计数，为0时自动释放内存）
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：hWnd - 窗口句柄（渲染结果会显示在这个窗口）
// 返回值：bool - 成功创建返回true，失败返回false
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述（定义交换链的属性，告诉系统如何创建交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值导致错误
    sd.BufferCount = 2;           // 缓冲区数量（2=双缓冲，避免画面闪烁）
    sd.BufferDesc.Width = 0;      // 缓冲区宽度（0=自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;     // 缓冲区高度（0=自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位色，含透明度）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60=60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;       // 绑定的窗口（渲染结果显示到该窗口）
    sd.SampleDesc.Count = 1;      // 多重采样数量（1=无抗锯齿，性能优先）
    sd.SampleDesc.Quality = 0;    // 采样质量（0=默认）
    sd.Windowed = TRUE;           // 窗口模式（TRUE=窗口，FALSE=全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台数据，性能最好）

    UINT createDeviceFlags = 0;   // 创建设备的标志（0=默认，调试时可加D3D11_CREATE_DEVICE_DEBUG）
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 调试模式（需安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的D3D版本（如11.0、10.0）
    // 支持的D3D版本列表（优先11.0，不支持则用10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };

    // 创建设备、设备上下文和交换链（DirectX核心函数）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE,  // 使用硬件加速（显卡渲染）
        nullptr, createDeviceFlags,         // 无软件渲染模块，创建标志
        featureLevelArray, 2,               // 支持的D3D版本列表及数量
        D3D11_SDK_VERSION, &sd,             // SDK版本，交换链描述
        &g_pSwapChain, &g_pd3dDevice,       // 输出交换链和设备
        &featureLevel, &g_pd3dDeviceContext // 输出支持的版本和设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,   // 软件渲染（性能较差，兼容旧设备）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象，避免内存泄漏
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标

    // 释放COM对象（按依赖顺序释放，避免资源冲突）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

// 主函数：程序入口，控制整个程序的生命周期
int main() {
    // -------------------------- 步骤1：DPI适配（解决高分辨率屏幕UI模糊问题） --------------------------
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知
    // 获取主显示器的DPI缩放比例（如4K屏幕可能为2.0，1080P可能为1.0）
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)  // 获取主显示器
    );

    // -------------------------- 步骤2：创建Windows窗口（ImGui需要依附的窗口载体） --------------------------
    // 定义窗口类（描述窗口的基本属性，如消息处理函数、图标等）
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格（使用专属设备上下文，避免绘图冲突）
        WndProc,                     // 消息处理函数
        0L, 0L,                      // 额外数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景等（用默认）
        L"ImGui Example",            // 窗口类名（自定义，后续创建窗口需使用）
        nullptr                      // 小图标（默认）
    };
    ::RegisterClassExW(&wc);  // 注册窗口类（向系统注册这个窗口类型）

    // 创建窗口（生成实际窗口）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名（对应注册的类）
        L"Dear ImGui DirectX11 Example",  // 窗口标题
        WS_OVERLAPPEDWINDOW,         // 窗口风格（标准窗口，带标题栏、关闭按钮等）
        100, 100,                    // 初始位置（屏幕左上角x=100，y=100）
        (int)(1280 * main_scale),    // 宽度（1280 * DPI缩放，适配高分辨率）
        (int)(800 * main_scale),     // 高度（800 * DPI缩放）
        nullptr, nullptr,            // 父窗口、菜单（无）
        wc.hInstance, nullptr        // 程序实例、额外参数
    );

    // -------------------------- 步骤3：初始化DirectX 11（创建渲染环境） --------------------------
    if (!CreateDeviceD3D(hwnd))  // 调用函数创建D3D设备和交换链，失败则清理资源并退出
    {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后默认隐藏，需手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保立即显示

    // -------------------------- 步骤4：初始化ImGui（配置UI环境） --------------------------
    IMGUI_CHECKVERSION();  // 检查ImGui版本（确保编译版本与运行时一致）
    ImGui::CreateContext(); // 创建ImGui上下文（UI的"全局环境"）
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象（管理输入输出，如键盘、帧率）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab操作UI）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启手柄导航（支持游戏手柄操作）

    // -------------------------- 步骤5：设置UI缩放（适配DPI，避免高分辨率下UI过小） --------------------------
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素（按钮、文本等）
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // -------------------------- 步骤6：初始化ImGui后端（连接ImGui与系统/渲染API） --------------------------
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端（处理窗口消息、输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端（负责渲染UI）

    // -------------------------- 步骤7：程序状态变量（控制UI显示） --------------------------
    bool show_demo_window = true;    // 是否显示ImGui演示窗口
    bool show_another_window = false; // 是否显示"另一个窗口"
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）

    // -------------------------- 步骤8：主循环（程序的核心，持续运行直到退出） --------------------------
    bool done = false;  // 控制循环是否结束（true=退出）
    while (!done)
    {
        // -------------------------- 8.1 处理窗口消息（如关闭、点击等） --------------------------
        MSG msg;  // 存储消息的结构体
        // 从消息队列中获取消息（PM_REMOVE表示获取后移除，避免重复处理）
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如键盘按键转字符）
            ::DispatchMessage(&msg);   // 分发消息到WndProc处理
            if (msg.message == WM_QUIT)  // 收到退出消息（如点击关闭按钮）
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出循环

        // -------------------------- 8.2 处理窗口遮挡（优化性能） --------------------------
        // 如果交换链被遮挡（如窗口被覆盖），且确认遮挡状态：
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10ms，减少CPU占用
            continue;     // 跳过本次循环，不渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // -------------------------- 8.3 处理窗口大小调整（避免画面拉伸） --------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)  // 如果有新的窗口尺寸
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标
            // 调整交换链缓冲区大小（匹配新窗口尺寸）
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标（适配新尺寸）
        }

        // -------------------------- 8.4 开始ImGui新帧（准备绘制UI） --------------------------
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧
        ImGui::NewFrame();          // ImGui核心准备（通知ImGui可以开始定义UI了）

        // -------------------------- 8.5 定义UI界面（核心：这里是你要显示的UI） --------------------------
        /**
            ImGui::Begin()函数说明：
            函数声明：bool Begin(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0);
            参数：
            - name：窗口标题（唯一标识，相同标题会合并窗口）
            - p_open：控制窗口是否显示的指针（关闭窗口时会将其设为false）
            - flags：窗口标志（组合使用，如禁用标题栏、禁止移动等）
        */
        bool i = true;  // 控制窗口是否显示（true=显示）
        // 创建一个自定义窗口：标题为"我的IMGui"，禁止标题栏（NoTitleBar）和移动（NoMove）
        ImGui::Begin("我的IMGui", &i);

        // 这里可以添加其他UI控件（如按钮、文本等），目前是空窗口
        // 例如：ImGui::Text("这是我的第一个ImGui窗口！");
        // 长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");

        // 带颜色的文本框
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        // 鼠标悬浮上去会显示悬浮文本框，悬浮文本框会显示52am
        HelpMarker("52am");

        // ImGui中通过PushStyleColor()临时修改按钮在不同状态下的颜色
        // 注意：每次PushStyleColor()后必须用PopStyleColor()恢复默认样式，否则会影响后续UI元素

        // 1. 修改按钮"正常状态"（未被鼠标悬停、未被点击）的背景色
        // 参数1：ImGuiCol_Button - 指定修改"按钮正常状态"的颜色
        // 参数2：{1.0f, 1.0f, 0.0f, 1.0f} - RGBA颜色值（每个分量范围0.0f~1.0f）
        //   R=1.0f（红色满值）、G=1.0f（绿色满值）、B=0.0f（蓝色无）→ 混合为黄色
        //   A=1.0f（透明度100%，完全不透明）
        ImGui::PushStyleColor(ImGuiCol_Button, { 1.0f,1.0f,0.0f, 1.0f });

        // 2. 修改按钮"鼠标悬停状态"（鼠标放在按钮上但未点击）的背景色
        // 参数1：ImGuiCol_ButtonHovered - 指定修改"按钮被悬停时"的颜色
        // 参数2：{1.0f, 0.0f, 0.0f, 1.0f} → 红色（R满值，G、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f, 1.0f });

        // 3. 修改按钮"激活状态"（鼠标按下按钮但未松开）的背景色
        // 参数1：ImGuiCol_ButtonActive - 指定修改"按钮被点击时"的颜色
        // 参数2：{0.0f, 1.0f, 0.0f, 1.0f} → 绿色（G满值，R、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f, 1.0f });
        
        if (ImGui::Button("anNiu")) {
            // 点击按钮执行的代码
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        ImGui::PopStyleColor(3);

        ImGui::End();  // 结束窗口定义（必须与Begin配对，否则崩溃）

        // -------------------------- 8.6 渲染UI（将定义的UI绘制到屏幕） --------------------------
        ImGui::Render();  // 生成绘制命令（将UI转换为显卡可执行的指令）

        // 计算背景色（考虑透明度：clear_color.w是透明度，乘以RGB值）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标（告诉显卡：接下来的绘制输出到主渲染目标）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空屏幕（用背景色填充，避免上一帧画面残留）
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        // 渲染ImGui的UI（执行绘制命令，将UI画到屏幕）
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // -------------------------- 8.7 显示画面（交换前后缓冲区，展示渲染结果） --------------------------
        // Present函数：交换前后缓冲区（后台缓冲区是刚渲染的画面，前台是正在显示的）
        // 参数1：1=开启垂直同步（VSync，防止画面撕裂，帧率与显示器一致）；0=关闭（帧率更高）
        HRESULT hr = g_pSwapChain->Present(1, 0);   // 开启垂直同步
        // HRESULT hr = g_pSwapChain->Present(0, 0); // 关闭垂直同步

        // 检查交换链是否被遮挡（用于后续优化）
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 步骤9：程序退出，清理资源 --------------------------
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 6. 6.ImGui-颜色（色板）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151192335
- Description: æç« æµè§éè¯»863æ¬¡ï¼ç¹èµ3æ¬¡ï¼æ¶è5æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui imvec4

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：5.ImGui-按钮 
IMGui中表示颜色的的结构体 
 
 ImVec4和ImU32，如下图红框 
  
 它们的用法 
 
```text
ImVec4 color4(1.0f, 0.0f, 0.0f, 1.0f)// RGBA值表示颜色，rgb是红绿蓝，a表示透明度，它的取值范围是0.0到1.0
ImU32 color32 = IM_COL32(255,0,0,255); // 使用IM_COL32将RGBA值转为ImU32类型，取值范围是0到255

```
 
 如下图使用Windows系统自带的画图软件，可以查看rgb的值，这个值对应ImU32的写法，ImVec4的写法是一种百分比的写法不够直观 
 
 
在我们的代码中使用ImU32 
 
色板从源码中找，如下图是源码中实例 
 
然后来到ImGui的源码中点击下图红框的按钮 
 
然后输入搜索关键字，如下图红框 
 
然后在搜索结果找到directx11的，双击它 
 
然后就找到了色板的代码，如下图红框 
 
色板的代码说明 
 
 ImGui::ColorEdit3这个会创建一个色板的控件，在控件里选择一个颜色后，会返回给&seBan这个变量 
 
```text
 ImGui::ColorEdit3("clear color", (float*)&seBan);

```
 
 色板的变量只能是 ImVec4类型，否则在色板中选择颜色会有问题 
  
 然后设置颜色 
 
 
完整代码

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：5.ImGui-按钮 
IMGui中表示颜色的的结构体 
 
 ImVec4和ImU32，如下图红框 
  
 它们的用法 
 
```text
ImVec4 color4(1.0f, 0.0f, 0.0f, 1.0f)// RGBA值表示颜色，rgb是红绿蓝，a表示透明度，它的取值范围是0.0到1.0
ImU32 color32 = IM_COL32(255,0,0,255); // 使用IM_COL32将RGBA值转为ImU32类型，取值范围是0到255

```
 
 如下图使用Windows系统自带的画图软件，可以查看rgb的值，这个值对应ImU32的写法，ImVec4的写法是一种百分比的写法不够直观 
 
 
在我们的代码中使用ImU32 
 
色板从源码中找，如下图是源码中实例 
 
然后来到ImGui的源码中点击下图红框的按钮 
 
然后输入搜索关键字，如下图红框 
 
然后在搜索结果找到directx11的，双击它 
 
然后就找到了色板的代码，如下图红框 
 
色板的代码说明 
 
 ImGui::ColorEdit3这个会创建一个色板的控件，在控件里选择一个颜色后，会返回给&seBan这个变量 
 
```text
 ImGui::ColorEdit3("clear color", (float*)&seBan);

```
 
 色板的变量只能是 ImVec4类型，否则在色板中选择颜色会有问题 
  
 然后设置颜色 
 
 
完整代码 

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

// 窗口消息处理函数：处理所有窗口事件（如点击、关闭、调整大小等）
// 参数：
// - hWnd：窗口句柄（标识当前窗口）
// - msg：消息类型（如WM_SIZE表示窗口大小改变）
// - wParam：消息附加参数（如WM_SIZE中表示 resize 类型）
// - lParam：消息附加参数（如WM_SIZE中存储新的宽高）
// 返回值：LRESULT类型（消息处理结果，0表示成功处理）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是ImGui的UI控件触发的事件，优先由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;  // ImGui已处理，直接返回

    // 根据消息类型处理不同事件
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        if (wParam == SIZE_MINIMIZED)  // 如果是窗口最小化，无需处理渲染相关
            return 0;
        // 从lParam中提取新的窗口尺寸：低16位是宽度，高16位是高度
        g_ResizeWidth = (UINT)LOWORD(lParam);  // 记录新宽度
        g_ResizeHeight = (UINT)HIWORD(lParam); // 记录新高度
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单（避免菜单遮挡ImGui控件，影响操作体验）
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标（ImGui绘制的内容会输出到这里）
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时存储交换链的后台缓冲区

    // 从交换链获取后台缓冲区（参数0表示第一个缓冲区，IID_ID3D11Texture2D指定缓冲区类型）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    // 用D3D设备创建渲染目标视图（将后台缓冲区转换为可渲染的目标）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    // 释放临时缓冲区（渲染目标视图已引用它，无需保留此指针）
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
void CleanupRenderTarget()
{
    // 释放渲染目标视图（COM对象需调用Release()减少引用计数，为0时自动释放内存）
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：hWnd - 窗口句柄（渲染结果会显示在这个窗口）
// 返回值：bool - 成功创建返回true，失败返回false
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述（定义交换链的属性，告诉系统如何创建交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值导致错误
    sd.BufferCount = 2;           // 缓冲区数量（2=双缓冲，避免画面闪烁）
    sd.BufferDesc.Width = 0;      // 缓冲区宽度（0=自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;     // 缓冲区高度（0=自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位色，含透明度）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60=60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;       // 绑定的窗口（渲染结果显示到该窗口）
    sd.SampleDesc.Count = 1;      // 多重采样数量（1=无抗锯齿，性能优先）
    sd.SampleDesc.Quality = 0;    // 采样质量（0=默认）
    sd.Windowed = TRUE;           // 窗口模式（TRUE=窗口，FALSE=全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台数据，性能最好）

    UINT createDeviceFlags = 0;   // 创建设备的标志（0=默认，调试时可加D3D11_CREATE_DEVICE_DEBUG）
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 调试模式（需安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的D3D版本（如11.0、10.0）
    // 支持的D3D版本列表（优先11.0，不支持则用10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };

    // 创建设备、设备上下文和交换链（DirectX核心函数）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE,  // 使用硬件加速（显卡渲染）
        nullptr, createDeviceFlags,         // 无软件渲染模块，创建标志
        featureLevelArray, 2,               // 支持的D3D版本列表及数量
        D3D11_SDK_VERSION, &sd,             // SDK版本，交换链描述
        &g_pSwapChain, &g_pd3dDevice,       // 输出交换链和设备
        &featureLevel, &g_pd3dDeviceContext // 输出支持的版本和设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,   // 软件渲染（性能较差，兼容旧设备）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象，避免内存泄漏
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标

    // 释放COM对象（按依赖顺序释放，避免资源冲突）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

// 主函数：程序入口，控制整个程序的生命周期
int main() {
    // -------------------------- 步骤1：DPI适配（解决高分辨率屏幕UI模糊问题） --------------------------
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知
    // 获取主显示器的DPI缩放比例（如4K屏幕可能为2.0，1080P可能为1.0）
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)  // 获取主显示器
    );

    // -------------------------- 步骤2：创建Windows窗口（ImGui需要依附的窗口载体） --------------------------
    // 定义窗口类（描述窗口的基本属性，如消息处理函数、图标等）
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格（使用专属设备上下文，避免绘图冲突）
        WndProc,                     // 消息处理函数
        0L, 0L,                      // 额外数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景等（用默认）
        L"ImGui Example",            // 窗口类名（自定义，后续创建窗口需使用）
        nullptr                      // 小图标（默认）
    };
    ::RegisterClassExW(&wc);  // 注册窗口类（向系统注册这个窗口类型）

    // 创建窗口（生成实际窗口）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名（对应注册的类）
        L"Dear ImGui DirectX11 Example",  // 窗口标题
        WS_OVERLAPPEDWINDOW,         // 窗口风格（标准窗口，带标题栏、关闭按钮等）
        100, 100,                    // 初始位置（屏幕左上角x=100，y=100）
        (int)(1280 * main_scale),    // 宽度（1280 * DPI缩放，适配高分辨率）
        (int)(800 * main_scale),     // 高度（800 * DPI缩放）
        nullptr, nullptr,            // 父窗口、菜单（无）
        wc.hInstance, nullptr        // 程序实例、额外参数
    );

    // -------------------------- 步骤3：初始化DirectX 11（创建渲染环境） --------------------------
    if (!CreateDeviceD3D(hwnd))  // 调用函数创建D3D设备和交换链，失败则清理资源并退出
    {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后默认隐藏，需手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保立即显示

    // -------------------------- 步骤4：初始化ImGui（配置UI环境） --------------------------
    IMGUI_CHECKVERSION();  // 检查ImGui版本（确保编译版本与运行时一致）
    ImGui::CreateContext(); // 创建ImGui上下文（UI的"全局环境"）
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象（管理输入输出，如键盘、帧率）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab操作UI）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启手柄导航（支持游戏手柄操作）

    // -------------------------- 步骤5：设置UI缩放（适配DPI，避免高分辨率下UI过小） --------------------------
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素（按钮、文本等）
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // -------------------------- 步骤6：初始化ImGui后端（连接ImGui与系统/渲染API） --------------------------
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端（处理窗口消息、输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端（负责渲染UI）

    // -------------------------- 步骤7：程序状态变量（控制UI显示） --------------------------
    bool show_demo_window = true;    // 是否显示ImGui演示窗口
    bool show_another_window = false; // 是否显示"另一个窗口"
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    //ImU32 seBan = IM_COL32(89, 255, 199, 255);
    // 初始化色板的颜色
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
    // -------------------------- 步骤8：主循环（程序的核心，持续运行直到退出） --------------------------
    bool done = false;  // 控制循环是否结束（true=退出）
    while (!done)
    {
        // -------------------------- 8.1 处理窗口消息（如关闭、点击等） --------------------------
        MSG msg;  // 存储消息的结构体
        // 从消息队列中获取消息（PM_REMOVE表示获取后移除，避免重复处理）
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如键盘按键转字符）
            ::DispatchMessage(&msg);   // 分发消息到WndProc处理
            if (msg.message == WM_QUIT)  // 收到退出消息（如点击关闭按钮）
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出循环

        // -------------------------- 8.2 处理窗口遮挡（优化性能） --------------------------
        // 如果交换链被遮挡（如窗口被覆盖），且确认遮挡状态：
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10ms，减少CPU占用
            continue;     // 跳过本次循环，不渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // -------------------------- 8.3 处理窗口大小调整（避免画面拉伸） --------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)  // 如果有新的窗口尺寸
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标
            // 调整交换链缓冲区大小（匹配新窗口尺寸）
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标（适配新尺寸）
        }

        // -------------------------- 8.4 开始ImGui新帧（准备绘制UI） --------------------------
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧
        ImGui::NewFrame();          // ImGui核心准备（通知ImGui可以开始定义UI了）

        // -------------------------- 8.5 定义UI界面（核心：这里是你要显示的UI） --------------------------
        /**
            ImGui::Begin()函数说明：
            函数声明：bool Begin(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0);
            参数：
            - name：窗口标题（唯一标识，相同标题会合并窗口）
            - p_open：控制窗口是否显示的指针（关闭窗口时会将其设为false）
            - flags：窗口标志（组合使用，如禁用标题栏、禁止移动等）
        */
        bool i = true;  // 控制窗口是否显示（true=显示）
        // 创建一个自定义窗口：标题为"我的IMGui"，禁止标题栏（NoTitleBar）和移动（NoMove）
        ImGui::Begin("我的IMGui", &i);

        // 这里可以添加其他UI控件（如按钮、文本等），目前是空窗口
        // 例如：ImGui::Text("这是我的第一个ImGui窗口！");
        // 长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");

        // 带颜色的文本框
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        // 鼠标悬浮上去会显示悬浮文本框，悬浮文本框会显示52am
        HelpMarker("52am");

        // ImGui::ColorEdit3这个会创建一个色板的控件，在控件里选择一个颜色后，会返回给&seBan这个变量
        ImGui::ColorEdit3("clear color", (float*)&seBan); // Edit 3 floats representing a color
        // ImGui中通过PushStyleColor()临时修改按钮在不同状态下的颜色
        // 注意：每次PushStyleColor()后必须用PopStyleColor()恢复默认样式，否则会影响后续UI元素

        // 1. 修改按钮"正常状态"（未被鼠标悬停、未被点击）的背景色
        // 参数1：ImGuiCol_Button - 指定修改"按钮正常状态"的颜色
        // 参数2：{1.0f, 1.0f, 0.0f, 1.0f} - RGBA颜色值（每个分量范围0.0f~1.0f）
        //   R=1.0f（红色满值）、G=1.0f（绿色满值）、B=0.0f（蓝色无）→ 混合为黄色
        //   A=1.0f（透明度100%，完全不透明）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);

        // 2. 修改按钮"鼠标悬停状态"（鼠标放在按钮上但未点击）的背景色
        // 参数1：ImGuiCol_ButtonHovered - 指定修改"按钮被悬停时"的颜色
        // 参数2：{1.0f, 0.0f, 0.0f, 1.0f} → 红色（R满值，G、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f, 1.0f });

        // 3. 修改按钮"激活状态"（鼠标按下按钮但未松开）的背景色
        // 参数1：ImGuiCol_ButtonActive - 指定修改"按钮被点击时"的颜色
        // 参数2：{0.0f, 1.0f, 0.0f, 1.0f} → 绿色（G满值，R、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f, 1.0f });
        
        if (ImGui::Button("anNiu")) {
            // 点击按钮执行的代码
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        ImGui::PopStyleColor(3);

     

        ImGui::End();  // 结束窗口定义（必须与Begin配对，否则崩溃）

        // -------------------------- 8.6 渲染UI（将定义的UI绘制到屏幕） --------------------------
        ImGui::Render();  // 生成绘制命令（将UI转换为显卡可执行的指令）

        // 计算背景色（考虑透明度：clear_color.w是透明度，乘以RGB值）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标（告诉显卡：接下来的绘制输出到主渲染目标）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空屏幕（用背景色填充，避免上一帧画面残留）
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        // 渲染ImGui的UI（执行绘制命令，将UI画到屏幕）
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // -------------------------- 8.7 显示画面（交换前后缓冲区，展示渲染结果） --------------------------
        // Present函数：交换前后缓冲区（后台缓冲区是刚渲染的画面，前台是正在显示的）
        // 参数1：1=开启垂直同步（VSync，防止画面撕裂，帧率与显示器一致）；0=关闭（帧率更高）
        HRESULT hr = g_pSwapChain->Present(1, 0);   // 开启垂直同步
        // HRESULT hr = g_pSwapChain->Present(0, 0); // 关闭垂直同步

        // 检查交换链是否被遮挡（用于后续优化）
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 步骤9：程序退出，清理资源 --------------------------
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 7. 7.ImGui-单选框和复选框

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151246860
- Description: æç« æµè§éè¯»1.2kæ¬¡ï¼ç¹èµ43æ¬¡ï¼æ¶è2æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui åéæ¡

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：6.ImGui-颜色（色板） 
如下图红框，源码中的实例 
 
点击下图红框位置 
 
搜索的内容 
 
搜索结果 
 
代码和界面的对应 
 
直接把它们赋值到我们的代码中 
 
效果图： 
 
完整代码

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：6.ImGui-颜色（色板） 
如下图红框，源码中的实例 
 
点击下图红框位置 
 
搜索的内容 
 
搜索结果 
 
代码和界面的对应 
 
直接把它们赋值到我们的代码中 
 
效果图： 
 
完整代码 

```text
#include "main.h"  // 包含程序所需的头文件（包含ImGui、DirectX等声明，具体内容在main.h中定义）

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享，方便各函数访问）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0; // 窗口调整大小时的新宽高（由消息处理函数记录，主循环处理）
static ID3D11Device* g_pd3dDevice = nullptr;                          // D3D11设备对象（核心！用于创建纹理、缓冲区等渲染资源）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;             // D3D11设备上下文（用于执行绘制、清空等渲染命令）
static IDXGISwapChain* g_pSwapChain = nullptr;                          // 交换链（双缓冲区机制，避免画面闪烁，负责显示渲染结果）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;        // 主渲染目标视图（绑定交换链的后台缓冲区，ImGui绘制的内容会输出到这里）
static bool                     g_SwapChainOccluded = false;           // 标记交换链是否被遮挡（如窗口被覆盖，用于优化性能）

// 声明ImGui的Win32消息处理函数（来自imgui_impl_win32.cpp，用于让ImGui处理鼠标/键盘输入）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");
    if (ImGui::BeginItemTooltip())
    {
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);
        ImGui::PopTextWrapPos();
        ImGui::EndTooltip();
    }
}

// 窗口消息处理函数：处理所有窗口事件（如点击、关闭、调整大小等）
// 参数：
// - hWnd：窗口句柄（标识当前窗口）
// - msg：消息类型（如WM_SIZE表示窗口大小改变）
// - wParam：消息附加参数（如WM_SIZE中表示 resize 类型）
// - lParam：消息附加参数（如WM_SIZE中存储新的宽高）
// 返回值：LRESULT类型（消息处理结果，0表示成功处理）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息（如果是ImGui的UI控件触发的事件，优先由ImGui处理）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;  // ImGui已处理，直接返回

    // 根据消息类型处理不同事件
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        if (wParam == SIZE_MINIMIZED)  // 如果是窗口最小化，无需处理渲染相关
            return 0;
        // 从lParam中提取新的窗口尺寸：低16位是宽度，高16位是高度
        g_ResizeWidth = (UINT)LOWORD(lParam);  // 记录新宽度
        g_ResizeHeight = (UINT)HIWORD(lParam); // 记录新高度
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单（避免菜单遮挡ImGui控件，影响操作体验）
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标（ImGui绘制的内容会输出到这里）
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时存储交换链的后台缓冲区

    // 从交换链获取后台缓冲区（参数0表示第一个缓冲区，IID_ID3D11Texture2D指定缓冲区类型）
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));
    // 用D3D设备创建渲染目标视图（将后台缓冲区转换为可渲染的目标）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    // 释放临时缓冲区（渲染目标视图已引用它，无需保留此指针）
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
void CleanupRenderTarget()
{
    // 释放渲染目标视图（COM对象需调用Release()减少引用计数，为0时自动释放内存）
    if (g_mainRenderTargetView) { g_mainRenderTargetView->Release(); g_mainRenderTargetView = nullptr; }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：hWnd - 窗口句柄（渲染结果会显示在这个窗口）
// 返回值：bool - 成功创建返回true，失败返回false
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述（定义交换链的属性，告诉系统如何创建交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免随机值导致错误
    sd.BufferCount = 2;           // 缓冲区数量（2=双缓冲，避免画面闪烁）
    sd.BufferDesc.Width = 0;      // 缓冲区宽度（0=自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;     // 缓冲区高度（0=自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位色，含透明度）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60=60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（如全屏/窗口）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;       // 绑定的窗口（渲染结果显示到该窗口）
    sd.SampleDesc.Count = 1;      // 多重采样数量（1=无抗锯齿，性能优先）
    sd.SampleDesc.Quality = 0;    // 采样质量（0=默认）
    sd.Windowed = TRUE;           // 窗口模式（TRUE=窗口，FALSE=全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台数据，性能最好）

    UINT createDeviceFlags = 0;   // 创建设备的标志（0=默认，调试时可加D3D11_CREATE_DEVICE_DEBUG）
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 调试模式（需安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的D3D版本（如11.0、10.0）
    // 支持的D3D版本列表（优先11.0，不支持则用10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0, };

    // 创建设备、设备上下文和交换链（DirectX核心函数）
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE,  // 使用硬件加速（显卡渲染）
        nullptr, createDeviceFlags,         // 无软件渲染模块，创建标志
        featureLevelArray, 2,               // 支持的D3D版本列表及数量
        D3D11_SDK_VERSION, &sd,             // SDK版本，交换链描述
        &g_pSwapChain, &g_pd3dDevice,       // 输出交换链和设备
        &featureLevel, &g_pd3dDeviceContext // 输出支持的版本和设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,   // 软件渲染（性能较差，兼容旧设备）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象，避免内存泄漏
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标

    // 释放COM对象（按依赖顺序释放，避免资源冲突）
    if (g_pSwapChain) { g_pSwapChain->Release(); g_pSwapChain = nullptr; }
    if (g_pd3dDeviceContext) { g_pd3dDeviceContext->Release(); g_pd3dDeviceContext = nullptr; }
    if (g_pd3dDevice) { g_pd3dDevice->Release(); g_pd3dDevice = nullptr; }
}

// 主函数：程序入口，控制整个程序的生命周期
int main() {
    // -------------------------- 步骤1：DPI适配（解决高分辨率屏幕UI模糊问题） --------------------------
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知
    // 获取主显示器的DPI缩放比例（如4K屏幕可能为2.0，1080P可能为1.0）
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)  // 获取主显示器
    );

    // -------------------------- 步骤2：创建Windows窗口（ImGui需要依附的窗口载体） --------------------------
    // 定义窗口类（描述窗口的基本属性，如消息处理函数、图标等）
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格（使用专属设备上下文，避免绘图冲突）
        WndProc,                     // 消息处理函数
        0L, 0L,                      // 额外数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景等（用默认）
        L"ImGui Example",            // 窗口类名（自定义，后续创建窗口需使用）
        nullptr                      // 小图标（默认）
    };
    ::RegisterClassExW(&wc);  // 注册窗口类（向系统注册这个窗口类型）

    // 创建窗口（生成实际窗口）
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名（对应注册的类）
        L"Dear ImGui DirectX11 Example",  // 窗口标题
        WS_OVERLAPPEDWINDOW,         // 窗口风格（标准窗口，带标题栏、关闭按钮等）
        100, 100,                    // 初始位置（屏幕左上角x=100，y=100）
        (int)(1280 * main_scale),    // 宽度（1280 * DPI缩放，适配高分辨率）
        (int)(800 * main_scale),     // 高度（800 * DPI缩放）
        nullptr, nullptr,            // 父窗口、菜单（无）
        wc.hInstance, nullptr        // 程序实例、额外参数
    );

    // -------------------------- 步骤3：初始化DirectX 11（创建渲染环境） --------------------------
    if (!CreateDeviceD3D(hwnd))  // 调用函数创建D3D设备和交换链，失败则清理资源并退出
    {
        CleanupDeviceD3D();
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后默认隐藏，需手动显示）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保立即显示

    // -------------------------- 步骤4：初始化ImGui（配置UI环境） --------------------------
    IMGUI_CHECKVERSION();  // 检查ImGui版本（确保编译版本与运行时一致）
    ImGui::CreateContext(); // 创建ImGui上下文（UI的"全局环境"）
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象（管理输入输出，如键盘、帧率）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab操作UI）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启手柄导航（支持游戏手柄操作）

    // -------------------------- 步骤5：设置UI缩放（适配DPI，避免高分辨率下UI过小） --------------------------
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素（按钮、文本等）
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // -------------------------- 步骤6：初始化ImGui后端（连接ImGui与系统/渲染API） --------------------------
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端（处理窗口消息、输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端（负责渲染UI）

    // -------------------------- 步骤7：程序状态变量（控制UI显示） --------------------------
    bool show_demo_window = true;    // 是否显示ImGui演示窗口
    bool show_another_window = false; // 是否显示"另一个窗口"
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    //ImU32 seBan = IM_COL32(89, 255, 199, 255);
    // 初始化色板的颜色
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
    // -------------------------- 步骤8：主循环（程序的核心，持续运行直到退出） --------------------------
    bool done = false;  // 控制循环是否结束（true=退出）
    while (!done)
    {
        // -------------------------- 8.1 处理窗口消息（如关闭、点击等） --------------------------
        MSG msg;  // 存储消息的结构体
        // 从消息队列中获取消息（PM_REMOVE表示获取后移除，避免重复处理）
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如键盘按键转字符）
            ::DispatchMessage(&msg);   // 分发消息到WndProc处理
            if (msg.message == WM_QUIT)  // 收到退出消息（如点击关闭按钮）
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出循环

        // -------------------------- 8.2 处理窗口遮挡（优化性能） --------------------------
        // 如果交换链被遮挡（如窗口被覆盖），且确认遮挡状态：
        if (g_SwapChainOccluded && g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10ms，减少CPU占用
            continue;     // 跳过本次循环，不渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // -------------------------- 8.3 处理窗口大小调整（避免画面拉伸） --------------------------
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)  // 如果有新的窗口尺寸
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标
            // 调整交换链缓冲区大小（匹配新窗口尺寸）
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight, DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标（适配新尺寸）
        }

        // -------------------------- 8.4 开始ImGui新帧（准备绘制UI） --------------------------
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧
        ImGui::NewFrame();          // ImGui核心准备（通知ImGui可以开始定义UI了）

        // -------------------------- 8.5 定义UI界面（核心：这里是你要显示的UI） --------------------------
        /**
            ImGui::Begin()函数说明：
            函数声明：bool Begin(const char* name, bool* p_open = NULL, ImGuiWindowFlags flags = 0);
            参数：
            - name：窗口标题（唯一标识，相同标题会合并窗口）
            - p_open：控制窗口是否显示的指针（关闭窗口时会将其设为false）
            - flags：窗口标志（组合使用，如禁用标题栏、禁止移动等）
        */
        bool i = true;  // 控制窗口是否显示（true=显示）
        // 创建一个自定义窗口：标题为"我的IMGui"，禁止标题栏（NoTitleBar）和移动（NoMove）
        ImGui::Begin("我的IMGui", &i);

        // 这里可以添加其他UI控件（如按钮、文本等），目前是空窗口
        // 例如：ImGui::Text("这是我的第一个ImGui窗口！");
        // 长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");

        // 带颜色的文本框
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        // 鼠标悬浮上去会显示悬浮文本框，悬浮文本框会显示52am
        HelpMarker("52am");

        // ImGui::ColorEdit3这个会创建一个色板的控件，在控件里选择一个颜色后，会返回给&seBan这个变量
        ImGui::ColorEdit3("clear color", (float*)&seBan); // Edit 3 floats representing a color
        // ImGui中通过PushStyleColor()临时修改按钮在不同状态下的颜色
        // 注意：每次PushStyleColor()后必须用PopStyleColor()恢复默认样式，否则会影响后续UI元素

        // 1. 修改按钮"正常状态"（未被鼠标悬停、未被点击）的背景色
        // 参数1：ImGuiCol_Button - 指定修改"按钮正常状态"的颜色
        // 参数2：{1.0f, 1.0f, 0.0f, 1.0f} - RGBA颜色值（每个分量范围0.0f~1.0f）
        //   R=1.0f（红色满值）、G=1.0f（绿色满值）、B=0.0f（蓝色无）→ 混合为黄色
        //   A=1.0f（透明度100%，完全不透明）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);

        // 2. 修改按钮"鼠标悬停状态"（鼠标放在按钮上但未点击）的背景色
        // 参数1：ImGuiCol_ButtonHovered - 指定修改"按钮被悬停时"的颜色
        // 参数2：{1.0f, 0.0f, 0.0f, 1.0f} → 红色（R满值，G、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f, 1.0f });

        // 3. 修改按钮"激活状态"（鼠标按下按钮但未松开）的背景色
        // 参数1：ImGuiCol_ButtonActive - 指定修改"按钮被点击时"的颜色
        // 参数2：{0.0f, 1.0f, 0.0f, 1.0f} → 绿色（G满值，R、B无），完全不透明
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f, 1.0f });
        
        if (ImGui::Button("anNiu")) {
            // 点击按钮执行的代码
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        ImGui::PopStyleColor(3);

     
        // 复选框默认值，true默认勾选，false默认不勾选
        static bool check = true;
        static bool check1 = true;
        static bool check2 = false;
        static bool check3 = true;
        /**
            通过鼠标点击复选框进行勾选，check的值会变成true
            使用鼠标对复选框进行取消勾选check的值会变成false
        */
        ImGui::Checkbox("checkbox", &check);
        ImGui::Checkbox("checkbox1", &check1);
        ImGui::Checkbox("checkbox2", &check2);
        ImGui::Checkbox("checkbox3", &check3);

        // 单选框默认勾选0，也就是默认勾选 radio a
        static int e = 0;
        // ("radio a", &e, 0) e是当前选中的单选框id，e的值是什么就选中什么单选框，0是当前单选框的id
        ImGui::RadioButton("radio a", &e, 0); ImGui::SameLine();
        ImGui::RadioButton("radio b", &e, 1); ImGui::SameLine();
        ImGui::RadioButton("radio c", &e, 2);

        ImGui::End();  // 结束窗口定义（必须与Begin配对，否则崩溃）

        // -------------------------- 8.6 渲染UI（将定义的UI绘制到屏幕） --------------------------
        ImGui::Render();  // 生成绘制命令（将UI转换为显卡可执行的指令）

        // 计算背景色（考虑透明度：clear_color.w是透明度，乘以RGB值）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标（告诉显卡：接下来的绘制输出到主渲染目标）
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空屏幕（用背景色填充，避免上一帧画面残留）
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView, clear_color_with_alpha);
        // 渲染ImGui的UI（执行绘制命令，将UI画到屏幕）
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // -------------------------- 8.7 显示画面（交换前后缓冲区，展示渲染结果） --------------------------
        // Present函数：交换前后缓冲区（后台缓冲区是刚渲染的画面，前台是正在显示的）
        // 参数1：1=开启垂直同步（VSync，防止画面撕裂，帧率与显示器一致）；0=关闭（帧率更高）
        HRESULT hr = g_pSwapChain->Present(1, 0);   // 开启垂直同步
        // HRESULT hr = g_pSwapChain->Present(0, 0); // 关闭垂直同步

        // 检查交换链是否被遮挡（用于后续优化）
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // -------------------------- 步骤9：程序退出，清理资源 --------------------------
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 8. 8.ImGui-输入框

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151280154
- Description: æç« æµè§éè¯»666æ¬¡ï¼ç¹èµ4æ¬¡ï¼æ¶è9æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui::inputtext

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：7.ImGui-单选框和复选框 
单行输入框使用 
 
 ImGui::InputText()，下图中使用的name和pass两个变量 
 char name[1024] = ""; 
 char pass[1024] = ""; 是这样的声明放在了循环外 
  
 name和pass声明 
  
 上方的图中InputText第一个参数里前面有两个#，这个原因是如下图红框，加两个#可以隐藏InputText第一个参数的文字 
 
 
带默认提示的单行输入框 
 
 使用ImGui::InputTextWithHint函数，通过第二个参数设置默认提示 
  
 输入文字后的效果 
 
 
多行输入框 
 
 使用 ImGui::InputTextMultiline 函数 
  
 它使用的BUF_SIZE和input_text变量的声明 
 
 
完整代码：

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

// 声明ImGui的Win32消息处理函数（定义在imgui_impl_win32.cpp中）
// 该函数用于让ImGui处理鼠标、键盘等输入消息
// 参数说明：
// - hWnd: 窗口句柄，标识接收消息的窗口
// - msg: 消息类型，如WM_MOUSEMOVE（鼠标移动）、WM_KEYDOWN（按键按下）等
// - wParam: 消息参数1，存储与消息相关的附加信息
// - lParam: 消息参数2，存储与消息相关的附加信息
// 返回值：如果消息被ImGui处理则返回true，否则返回false
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：7.ImGui-单选框和复选框 
单行输入框使用 
 
 ImGui::InputText()，下图中使用的name和pass两个变量 
 char name[1024] = ""; 
 char pass[1024] = ""; 是这样的声明放在了循环外 
  
 name和pass声明 
  
 上方的图中InputText第一个参数里前面有两个#，这个原因是如下图红框，加两个#可以隐藏InputText第一个参数的文字 
 
 
带默认提示的单行输入框 
 
 使用ImGui::InputTextWithHint函数，通过第二个参数设置默认提示 
  
 输入文字后的效果 
 
 
多行输入框 
 
 使用 ImGui::InputTextMultiline 函数 
  
 它使用的BUF_SIZE和input_text变量的声明 
 
 
完整代码： 

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

// 声明ImGui的Win32消息处理函数（定义在imgui_impl_win32.cpp中）
// 该函数用于让ImGui处理鼠标、键盘等输入消息
// 参数说明：
// - hWnd: 窗口句柄，标识接收消息的窗口
// - msg: 消息类型，如WM_MOUSEMOVE（鼠标移动）、WM_KEYDOWN（按键按下）等
// - wParam: 消息参数1，存储与消息相关的附加信息
// - lParam: 消息参数2，存储与消息相关的附加信息
// 返回值：如果消息被ImGui处理则返回true，否则返回false
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 自定义辅助函数：创建带提示的帮助标记
// 当鼠标悬停在"(?)"上时，会显示提示文本
// 参数：
// - desc: 要显示的提示文本内容
static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");  // 显示灰色的"(?)"作为帮助标记
    // 检查鼠标是否悬停在当前项目上，并开始绘制提示框
    if (ImGui::BeginItemTooltip())
    {
        // 设置文本自动换行的宽度（为字体大小的35倍）
        // 避免提示文本过长导致超出窗口范围
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);  // 显示提示文本（无格式）
        ImGui::PopTextWrapPos();       // 恢复文本换行设置
        ImGui::EndTooltip();           // 结束提示框绘制
    }
}

// 窗口消息处理函数：处理所有与窗口相关的事件
// 包括窗口大小改变、关闭、鼠标键盘输入等
// 参数说明：
// - hWnd: 窗口句柄，标识当前接收消息的窗口
// - msg: 消息类型，Windows系统定义的消息编号
// - wParam: 消息参数1，具体含义取决于消息类型
// - lParam: 消息参数2，具体含义取决于消息类型
// 返回值：LRESULT类型，消息处理的结果
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息，优先处理UI相关的输入事件
    // 如果ImGui处理了该消息（如点击UI控件），则直接返回
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 根据消息类型进行不同处理
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        // 如果是窗口最小化，则不需要调整渲染资源
        if (wParam == SIZE_MINIMIZED)
            return 0;
        // 从lParam中提取新的窗口宽度和高度
        // LOWORD宏获取lParam的低16位，存储宽度
        // HIWORD宏获取lParam的高16位，存储高度
        g_ResizeWidth = (UINT)LOWORD(lParam);
        g_ResizeHeight = (UINT)HIWORD(lParam);
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单，避免菜单弹出时遮挡ImGui控件
        // SC_KEYMENU是系统菜单命令，0xfff0用于屏蔽低位的扩展信息
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标
// 渲染目标视图是GPU可以写入的资源视图
// 所有的渲染命令最终都会绘制到该渲染目标上
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时指针，用于获取后台缓冲区

    // 从交换链中获取后台缓冲区
    // 参数1：0表示获取第一个缓冲区（交换链通常有2个缓冲区）
    // 参数2：IID_ID3D11Texture2D是要获取的接口ID
    // 参数3：输出参数，接收后台缓冲区的指针
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    // 使用D3D设备创建渲染目标视图
    // 参数1：要绑定为渲染目标的纹理（这里是后台缓冲区）
    // 参数2：渲染目标视图的描述（nullptr表示使用默认设置）
    // 参数3：输出参数，接收创建的渲染目标视图
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);

    // 释放临时的后台缓冲区指针
    // 渲染目标视图已经引用了该缓冲区，不需要再保留此指针
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
// COM对象需要通过Release()方法释放，减少引用计数
// 当引用计数为0时，对象会被自动销毁
void CleanupRenderTarget()
{
    if (g_mainRenderTargetView)
    {
        g_mainRenderTargetView->Release();  // 释放渲染目标视图
        g_mainRenderTargetView = nullptr;   // 置空指针，避免野指针
    }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：
// - hWnd: 窗口句柄，渲染结果将显示在该窗口中
// 返回值：bool类型，true表示创建成功，false表示失败
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述结构体，定义交换链的属性
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免未初始化的内存导致错误

    // 配置交换链参数
    sd.BufferCount = 2;                   // 缓冲区数量，2表示双缓冲
    sd.BufferDesc.Width = 0;              // 缓冲区宽度，0表示自动匹配窗口宽度
    sd.BufferDesc.Height = 0;             // 缓冲区高度，0表示自动匹配窗口高度
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式，32位RGBA（8位/通道）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子，60表示60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母，60/1=60Hz
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（窗口/全屏）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途，作为渲染目标
    sd.OutputWindow = hWnd;               // 绑定的窗口，渲染结果显示到该窗口
    sd.SampleDesc.Count = 1;              // 多重采样数量，1表示无抗锯齿
    sd.SampleDesc.Quality = 0;            // 采样质量，0表示默认
    sd.Windowed = TRUE;                   // 窗口模式，TRUE表示窗口化，FALSE表示全屏
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果，交换后丢弃后台缓冲区数据

    UINT createDeviceFlags = 0;  // 创建设备的标志
    // 调试模式开关，需要安装DirectX SDK才能使用
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的Direct3D特性级别（版本）
    // 支持的Direct3D版本列表，优先使用11.0，不支持则使用10.0
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_0
    };

    // 创建设备、设备上下文和交换链
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr,                       // 显卡适配器，nullptr表示使用默认显卡
        D3D_DRIVER_TYPE_HARDWARE,      // 驱动类型，硬件加速（使用GPU）
        nullptr,                       // 软件渲染模块，不需要则为nullptr
        createDeviceFlags,             // 创建设备的标志
        featureLevelArray,             // 支持的Direct3D版本列表
        2,                             // 版本列表的数量
        D3D11_SDK_VERSION,             // SDK版本，使用当前版本
        &sd,                           // 交换链描述结构体
        &g_pSwapChain,                 // 输出参数，接收创建的交换链
        &g_pd3dDevice,                 // 输出参数，接收创建的D3D设备
        &featureLevel,                 // 输出参数，接收实际支持的Direct3D版本
        &g_pd3dDeviceContext           // 输出参数，接收创建的设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试使用软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,  // 软件渲染驱动
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 如果创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象
// 按照依赖顺序释放，避免资源引用冲突
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标视图

    // 释放交换链
    if (g_pSwapChain)
    {
        g_pSwapChain->Release();
        g_pSwapChain = nullptr;
    }
    // 释放设备上下文
    if (g_pd3dDeviceContext)
    {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = nullptr;
    }
    // 释放D3D设备
    if (g_pd3dDevice)
    {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
    }
}

// 主函数：程序入口点，控制整个程序的生命周期
int main() {
    // DPI适配：解决高分辨率屏幕下UI模糊的问题
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知

    // 获取主显示器的DPI缩放比例
    // MonitorFromPoint获取主显示器的句柄
    // ImGui_ImplWin32_GetDpiScaleForMonitor计算该显示器的缩放比例
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)
    );

    // 创建Windows窗口：ImGui需要一个窗口作为载体来显示UI
    // 定义窗口类结构，描述窗口的基本属性
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格，使用专属设备上下文
        WndProc,                     // 窗口消息处理函数
        0L, 0L,                      // 额外的类数据和窗口数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景画刷等（使用默认）
        L"ImGui Example",            // 窗口类名，用于标识该窗口类
        nullptr                      // 小图标（使用默认）
    };
    ::RegisterClassExW(&wc);  // 向系统注册窗口类

    // 创建窗口
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名，必须与注册的类名一致
        L"Dear ImGui DirectX11 Example",  // 窗口标题栏显示的文本
        WS_OVERLAPPEDWINDOW,         // 窗口风格，标准可调整大小的窗口
        100, 100,                    // 窗口初始位置（屏幕左上角坐标）
        (int)(1280 * main_scale),    // 窗口宽度，根据DPI缩放
        (int)(800 * main_scale),     // 窗口高度，根据DPI缩放
        nullptr, nullptr,            // 父窗口句柄和菜单句柄（无）
        wc.hInstance, nullptr        // 程序实例句柄和额外数据（无）
    );

    // 初始化DirectX 11渲染环境
    if (!CreateDeviceD3D(hwnd))  // 如果创建失败
    {
        CleanupDeviceD3D();  // 清理已创建的资源
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);  // 注销窗口类
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后窗口默认是隐藏的）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保窗口立即显示

    // 初始化ImGui：创建UI上下文和配置
    IMGUI_CHECKVERSION();  // 检查ImGui版本，确保编译版本与运行时版本一致
    ImGui::CreateContext(); // 创建ImGui上下文，管理UI状态和资源
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象，管理输入输出

    // 配置ImGui功能
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab等）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启游戏手柄导航

    // 设置UI缩放：适配高DPI屏幕，避免UI元素过小
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素的大小
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // 初始化ImGui后端：连接ImGui与系统和渲染API
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端，处理窗口消息和输入
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端，负责渲染UI

    // 程序状态变量：控制UI显示和存储用户输入数据
    bool show_demo_window = true;    // 是否显示ImGui演示窗口（未使用）
    bool show_another_window = false; // 是否显示另一个窗口（未使用）
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);       // 用于按钮颜色的变量

    // 输入框缓冲区：存储用户输入的文本
    char name[1024] = "";    // 用户名输入缓冲区，容量1024字节
    char pass[1024] = "";    // 密码输入缓冲区，容量1024字节
    char text[1024] = "";    // 备用文本缓冲区（未使用）

    // 多行输入框配置
    const size_t BUF_SIZE = 1024;                // 缓冲区最大容量
    char input_text[BUF_SIZE] = "1111...\n22222\n333";  // 初始文本内容

    // 主循环：程序的核心，持续运行直到用户关闭窗口
    bool done = false;  // 控制循环是否结束的标志
    while (!done)
    {
        // 处理窗口消息：从消息队列中获取并处理所有待处理消息
        MSG msg;
        // PeekMessage非阻塞地获取消息，PM_REMOVE表示获取后从队列中移除
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如将键盘扫描码转换为字符）
            ::DispatchMessage(&msg);   // 将消息分发到窗口的消息处理函数（WndProc）
            if (msg.message == WM_QUIT)  // 如果收到退出消息
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出主循环

        // 处理窗口遮挡：如果窗口被完全遮挡，减少渲染频率以节省资源
        if (g_SwapChainOccluded &&
            g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10毫秒
            continue;     // 跳过本次循环，不进行渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // 处理窗口大小调整：当窗口大小改变时，调整渲染目标
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标

            // 调整交换链缓冲区大小以匹配新的窗口尺寸
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight,
                DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标

        }

        // 开始ImGui新帧：准备绘制UI
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧（处理输入）
        ImGui::NewFrame();          // ImGui核心准备，开始定义UI

        // 定义UI界面：创建一个名为"我的IMGui"的窗口
        bool is_window_open = true;  // 控制窗口是否显示的标志
        // ImGui::Begin()参数说明：
        // - 第一个参数：窗口标题，同时作为窗口的唯一标识
        // - 第二个参数：控制窗口是否显示的指针，关闭窗口时会设为false
        // - 第三个参数：窗口标志（默认为0，使用默认窗口样式）
        ImGui::Begin("我的IMGui", &is_window_open);

        // 显示自动换行的长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        // 显示带颜色的文本
        // ImGui::TextColored()参数：
        // - 第一个参数：ImVec4类型的颜色（RGBA，每个分量0.0f-1.0f）
        // - 后续参数：格式化字符串和参数（与printf类似）
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");  // 粉色文本
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");  // 黄色文本

        // 显示带颜色的文本和帮助标记，并在同一行
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();  // 让下一个控件与当前控件在同一行
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        HelpMarker("52am");  // 显示帮助标记，鼠标悬停显示"52am"

        // 颜色编辑控件：允许用户选择颜色
        // ImGui::ColorEdit3()参数：
        // - 第一个参数：控件标签
        // - 第二个参数：颜色变量的指针（需要转换为float*）
        // 选择的颜色会存储到seBan变量中
        ImGui::ColorEdit3("clear color", (float*)&seBan);

        // 修改按钮样式：临时改变按钮在不同状态下的颜色
        // ImGui::PushStyleColor()参数：
        // - 第一个参数：要修改的颜色类型（ImGuiCol_开头的枚举）
        // - 第二个参数：新的颜色值（ImVec4类型）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);           // 按钮正常状态颜色
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f,1.0f }); // 鼠标悬停状态
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f,1.0f });  // 鼠标点击状态

        // 创建按钮：ImGui::Button()返回bool值，表示按钮是否被点击
        if (ImGui::Button("anNiu")) {
            // 按钮被点击时，显示黄色文本"dianjianniu"
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        // 恢复样式：弹出之前压入的3个颜色设置
        // 必须与PushStyleColor的数量一致，否则会影响其他UI元素
        ImGui::PopStyleColor(3);

        // 复选框：允许用户切换选项的开关状态
        // ImGui::Checkbox()参数：
        // - 第一个参数：复选框标签
        // - 第二个参数：bool变量的指针，存储复选框的状态（true=勾选，false=未勾选）
        static bool check = true;
        static bool check1 = true;
        static bool check2 = false;
        static bool check3 = true;
        ImGui::Checkbox("checkbox", &check);
        ImGui::Checkbox("checkbox1", &check1);
        ImGui::Checkbox("checkbox2", &check2);
        ImGui::Checkbox("checkbox3", &check3);

        // 单选框：从多个选项中选择一个
        // ImGui::RadioButton()参数：
        // - 第一个参数：单选框标签
        // - 第二个参数：当前选中项的索引指针
        // - 第三个参数：当前单选框的索引值
        static int radio_selected = 0;  // 存储选中项的索引
        ImGui::RadioButton("radio a", &radio_selected, 0); ImGui::SameLine();
        ImGui::RadioButton("radio b", &radio_selected, 1); ImGui::SameLine();
        ImGui::RadioButton("radio c", &radio_selected, 2);

        // 输入框：接收用户文本输入
        ImGui::Text("name");  // 显示"name"作为输入框的标签
        ImGui::SameLine();    // 与输入框在同一行

        // ImGui输入框的标识规则详解：
        // 1. 格式为"标签##标识符"：显示"标签"，但内部用"标识符"区分不同控件
        // 2. 格式为"##标识符"：不显示标签，仅用"标识符"作为内部标识
        // 3. 无"##"：整个字符串既作为显示标签，也作为内部标识
        // 这里"##name"表示：不显示标签，内部用"name"作为标识
        ImGui::InputText("##name", name, IM_ARRAYSIZE(name));

        ImGui::Text("pass");  // 显示"pass"作为密码框的标签
        ImGui::SameLine();
        // 密码输入框：ImGuiInputTextFlags_Password标志使输入内容显示为*
        ImGui::InputText("##pass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);
        ImGui::InputText("p2ass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);

        // 带提示的输入框：当输入框为空时显示提示文本
        char hint_text[1024] = "mo ren ti shi";  // 提示文本
        ImGui::InputTextWithHint("##InputTextWithHint", hint_text,
            name, IM_ARRAYSIZE(name));

        // 多行输入框：允许输入多行文本
        ImGui::InputTextMultiline(
            "##MultiLineInput",  // 内部标识（不显示标签）
            input_text,          // 存储文本的缓冲区
            BUF_SIZE,            // 缓冲区最大容量
            ImVec2(0, 200)       // 输入框尺寸（宽度0表示自适应窗口，高度200像素）
        );

        ImGui::End();  // 结束窗口定义（必须与ImGui::Begin配对使用）

        // 渲染UI：将定义的UI绘制到屏幕上
        ImGui::Render();  // 生成绘制命令列表

        // 计算背景色（考虑透明度）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标：告诉GPU接下来的渲染输出到主渲染目标
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空渲染目标：用背景色填充屏幕，清除上一帧的内容
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView,
            clear_color_with_alpha);
        // 渲染ImGui的UI：执行绘制命令
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // 显示画面：交换前后缓冲区，将渲染好的画面显示到屏幕上
        // Present()参数：
        // - 第一个参数：1表示开启垂直同步（VSync），0表示关闭
        // - 第二个参数：交换标志（0表示默认行为）
        HRESULT hr = g_pSwapChain->Present(1, 0);  // 开启垂直同步
        // 检查交换链是否被遮挡，用于下一次循环的优化
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // 程序退出：清理所有资源
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 9. 9.ImGui-滑块

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151330153
- Description: æç« æµè§éè¯»411æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ_imgui slider

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：8.ImGui-输入框 
下图红框的就是滑块 
 
然后开始找它的代码，首先点击下图红框 
 
然后输入下图红框的内容，Another Window 
 
然后下图红框的就是Another Window复选框了，然后双击它 
 
然后就找到了滑块的代码，如下图红框，然后把它复制到我们的代码中 
 
效果图：

```text
// 加static让f变成静态变量，静态变量在函数中只会执行一次
// 第一次执行当前函数会执行 static float f = 0.0f; 这一行代码，第二次执行当前函数时会跳过 static float f = 0.0f;这一行代码
// 这样就能修改f的值后不会被重新赋值成0了
static float f = 0.0f;
// 滑块，下方代码滑块的数据范围是0.0到1.0
ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
ImGui::SliderFloat("##float", &f, 0.0f, 1.0f);

```
 
ImGui::SliderFloat它一共有6个参数，有两个参数有默认值"%.3f"和0，上方代码中只使用了4个参数，后面两个使用的默认值，它最后一个参数可以设置滑块的类型 
 
滑块类型的值如下

```text
/**
 * ImGuiSliderFlags_ 枚举：控制滑动条(SliderXXX)和拖动控件(DragXXX)的行为特性
 * 可通过 | 运算符组合多个标志（例如：ImGuiSliderFlags_Logarithmic | ImGuiSliderFlags_NoInput）
 */
enum ImGuiSliderFlags_
{
    /**
     * 作用：默认值，无任何特殊行为，使用ImGui的默认规则
     * 默认行为包括：
     * - 数值线性变化
     * - 支持Ctrl+Click或Enter手动输入文本
     * - 数值会按显示格式字符串的精度四舍五入
     * - 拖动时会被限制在min/max范围内（手动输入默认允许超出）
     * 适用场景：不需要自定义控件行为的基础场景
     */
    ImGuiSliderFlags_None               = 0,

/**
     * 作用：使控件数值按对数规律变化（默认是线性变化）
     * 区别：
     * - 线性变化：数值均匀增减（如1→2→3→4）
     * - 对数变化：小值时变化慢、大值时变化快（如1→2→4→8，符合比例感知）
     * 适用场景：
     * - 音量调节（人耳对音量是对数感知）
     * - 频率、缩放比例等需要"比例精度"的参数
     * 注意事项：
     * - 若使用显示格式字符串（如%.1f），建议搭配ImGuiSliderFlags_NoRoundToFormat
     * - 避免因格式精度不足导致数值被过度四舍五入
     */
    ImGuiSliderFlags_Logarithmic        = 1 << 5,

/**
     * 作用：禁用"按显示格式精度四舍五入数值"的默认行为
     * 示例：
     * - 默认：格式为%.1f时，实际值1.234会被四舍五入为1.2
     * - 启用后：实际值保持1.234，显示时按%.1f展示为1.2（内部精度不变）
     * 适用场景：
     * - 需要高精度存储但简化显示的场景（如科学计算参数）
     * - 需保留原始数值精度的精细调节场景
     */
    ImGuiSliderFlags_NoRoundToFormat    = 1 << 6,

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：8.ImGui-输入框 
下图红框的就是滑块 
 
然后开始找它的代码，首先点击下图红框 
 
然后输入下图红框的内容，Another Window 
 
然后下图红框的就是Another Window复选框了，然后双击它 
 
然后就找到了滑块的代码，如下图红框，然后把它复制到我们的代码中 
 
效果图： 
 

```text
// 加static让f变成静态变量，静态变量在函数中只会执行一次
// 第一次执行当前函数会执行 static float f = 0.0f; 这一行代码，第二次执行当前函数时会跳过 static float f = 0.0f;这一行代码
// 这样就能修改f的值后不会被重新赋值成0了
static float f = 0.0f;
// 滑块，下方代码滑块的数据范围是0.0到1.0
ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
ImGui::SliderFloat("##float", &f, 0.0f, 1.0f);

```
 
ImGui::SliderFloat它一共有6个参数，有两个参数有默认值"%.3f"和0，上方代码中只使用了4个参数，后面两个使用的默认值，它最后一个参数可以设置滑块的类型 
 
滑块类型的值如下 

```text
/**
 * ImGuiSliderFlags_ 枚举：控制滑动条(SliderXXX)和拖动控件(DragXXX)的行为特性
 * 可通过 | 运算符组合多个标志（例如：ImGuiSliderFlags_Logarithmic | ImGuiSliderFlags_NoInput）
 */
enum ImGuiSliderFlags_
{
    /**
     * 作用：默认值，无任何特殊行为，使用ImGui的默认规则
     * 默认行为包括：
     * - 数值线性变化
     * - 支持Ctrl+Click或Enter手动输入文本
     * - 数值会按显示格式字符串的精度四舍五入
     * - 拖动时会被限制在min/max范围内（手动输入默认允许超出）
     * 适用场景：不需要自定义控件行为的基础场景
     */
    ImGuiSliderFlags_None               = 0,

    /**
     * 作用：使控件数值按对数规律变化（默认是线性变化）
     * 区别：
     * - 线性变化：数值均匀增减（如1→2→3→4）
     * - 对数变化：小值时变化慢、大值时变化快（如1→2→4→8，符合比例感知）
     * 适用场景：
     * - 音量调节（人耳对音量是对数感知）
     * - 频率、缩放比例等需要"比例精度"的参数
     * 注意事项：
     * - 若使用显示格式字符串（如%.1f），建议搭配ImGuiSliderFlags_NoRoundToFormat
     * - 避免因格式精度不足导致数值被过度四舍五入
     */
    ImGuiSliderFlags_Logarithmic        = 1 << 5,      

    /**
     * 作用：禁用"按显示格式精度四舍五入数值"的默认行为
     * 示例：
     * - 默认：格式为%.1f时，实际值1.234会被四舍五入为1.2
     * - 启用后：实际值保持1.234，显示时按%.1f展示为1.2（内部精度不变）
     * 适用场景：
     * - 需要高精度存储但简化显示的场景（如科学计算参数）
     * - 需保留原始数值精度的精细调节场景
     */
    ImGuiSliderFlags_NoRoundToFormat    = 1 << 6,      

    /**
     * 作用：禁用手动输入文本功能，仅允许通过鼠标拖动改变数值
     * 默认行为：点击控件后按Enter或Ctrl+Click可弹出文本框手动输入
     * 适用场景：
     * - 不允许输入超出预期范围的数值（如安全参数0~10，禁止输入100）
     * - 只能按固定步长变化的参数（如整数调节，禁止输入小数）
     */
    ImGuiSliderFlags_NoInput            = 1 << 7,      

    /**
     * 作用：启用循环包裹功能，拖动到最大值时自动跳回最小值，反之亦然
     * 示例：
     * - 角度调节（0~360°）：拖到360°后继续拖会回到0°
     * - 月份调节（1~12）：拖到12后继续拖会回到1
     * 适用场景：数值本身具有循环特性的参数（角度、周期、序号等）
     * 注意事项：目前仅支持DragXXX系列函数（如DragInt），不支持SliderXXX
     */
    ImGuiSliderFlags_WrapAround         = 1 << 8,      

    /**
     * 作用：手动输入数值时，强制将数值限制在min~max范围内（夹紧）
     * 默认行为：手动输入允许超出min/max（拖动时才会被夹紧）
     * 示例：范围0~10，手动输入15会被自动改为10
     * 适用场景：需要严格限制范围的参数（如音量0~100、亮度0~255）
     */
    ImGuiSliderFlags_ClampOnInput       = 1 << 9,      

    /**
     * 作用：即使min==max==0.0f，也强制启用夹紧功能
     * 默认问题：因历史原因，当min和max都为0时，DragXXX默认不夹紧，可能被拖到非0值
     * 适用场景：
     * - 动态范围参数（默认0~0禁止修改，后续可能改为0~10）
     * - 需严格锁定数值为0的场景
     */
    ImGuiSliderFlags_ClampZeroRange     = 1 << 10,     

    /**
     * 作用：禁用键盘修饰键（Ctrl/Shift）对拖动速度的影响，保持固定速度
     * 默认行为：
     * - 按住Ctrl：拖动速度变慢（精细调节）
     * - 按住Shift：拖动速度变快（快速调节）
     * 适用场景：需要自定义拖动速度逻辑的场景（如根据范围自动调整速度）
     */
    ImGuiSliderFlags_NoSpeedTweaks      = 1 << 11,     

    /**
     * 作用：组合标志，同时启用ClampOnInput和ClampZeroRange的功能
     * 等价于：ImGuiSliderFlags_ClampOnInput | ImGuiSliderFlags_ClampZeroRange
     * 适用场景：需要严格夹紧的场景（手动输入+0~0范围都限制）
     */
    ImGuiSliderFlags_AlwaysClamp        = ImGuiSliderFlags_ClampOnInput | ImGuiSliderFlags_ClampZeroRange,

    /**
     * 作用：内部标志，用于检测API误用，用户禁止使用
     * 功能：检查是否有旧版API的参数（如float power）被错误转换为该枚举
     * 注意：普通用户不要在代码中使用，误用会触发调试断言
     */
    ImGuiSliderFlags_InvalidMask_       = 0x7000000F,   
};

```
 
完整代码： 

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

// 声明ImGui的Win32消息处理函数（定义在imgui_impl_win32.cpp中）
// 该函数用于让ImGui处理鼠标、键盘等输入消息
// 参数说明：
// - hWnd: 窗口句柄，标识接收消息的窗口
// - msg: 消息类型，如WM_MOUSEMOVE（鼠标移动）、WM_KEYDOWN（按键按下）等
// - wParam: 消息参数1，存储与消息相关的附加信息
// - lParam: 消息参数2，存储与消息相关的附加信息
// 返回值：如果消息被ImGui处理则返回true，否则返回false
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 自定义辅助函数：创建带提示的帮助标记
// 当鼠标悬停在"(?)"上时，会显示提示文本
// 参数：
// - desc: 要显示的提示文本内容
static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");  // 显示灰色的"(?)"作为帮助标记
    // 检查鼠标是否悬停在当前项目上，并开始绘制提示框
    if (ImGui::BeginItemTooltip())
    {
        // 设置文本自动换行的宽度（为字体大小的35倍）
        // 避免提示文本过长导致超出窗口范围
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);  // 显示提示文本（无格式）
        ImGui::PopTextWrapPos();       // 恢复文本换行设置
        ImGui::EndTooltip();           // 结束提示框绘制
    }
}

// 窗口消息处理函数：处理所有与窗口相关的事件
// 包括窗口大小改变、关闭、鼠标键盘输入等
// 参数说明：
// - hWnd: 窗口句柄，标识当前接收消息的窗口
// - msg: 消息类型，Windows系统定义的消息编号
// - wParam: 消息参数1，具体含义取决于消息类型
// - lParam: 消息参数2，具体含义取决于消息类型
// 返回值：LRESULT类型，消息处理的结果
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息，优先处理UI相关的输入事件
    // 如果ImGui处理了该消息（如点击UI控件），则直接返回
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 根据消息类型进行不同处理
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        // 如果是窗口最小化，则不需要调整渲染资源
        if (wParam == SIZE_MINIMIZED)
            return 0;
        // 从lParam中提取新的窗口宽度和高度
        // LOWORD宏获取lParam的低16位，存储宽度
        // HIWORD宏获取lParam的高16位，存储高度
        g_ResizeWidth = (UINT)LOWORD(lParam);
        g_ResizeHeight = (UINT)HIWORD(lParam);
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单，避免菜单弹出时遮挡ImGui控件
        // SC_KEYMENU是系统菜单命令，0xfff0用于屏蔽低位的扩展信息
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标
// 渲染目标视图是GPU可以写入的资源视图
// 所有的渲染命令最终都会绘制到该渲染目标上
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时指针，用于获取后台缓冲区

    // 从交换链中获取后台缓冲区
    // 参数1：0表示获取第一个缓冲区（交换链通常有2个缓冲区）
    // 参数2：IID_ID3D11Texture2D是要获取的接口ID
    // 参数3：输出参数，接收后台缓冲区的指针
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    // 使用D3D设备创建渲染目标视图
    // 参数1：要绑定为渲染目标的纹理（这里是后台缓冲区）
    // 参数2：渲染目标视图的描述（nullptr表示使用默认设置）
    // 参数3：输出参数，接收创建的渲染目标视图
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);

    // 释放临时的后台缓冲区指针
    // 渲染目标视图已经引用了该缓冲区，不需要再保留此指针
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
// COM对象需要通过Release()方法释放，减少引用计数
// 当引用计数为0时，对象会被自动销毁
void CleanupRenderTarget()
{
    if (g_mainRenderTargetView)
    {
        g_mainRenderTargetView->Release();  // 释放渲染目标视图
        g_mainRenderTargetView = nullptr;   // 置空指针，避免野指针
    }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：
// - hWnd: 窗口句柄，渲染结果将显示在该窗口中
// 返回值：bool类型，true表示创建成功，false表示失败
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述结构体，定义交换链的属性
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免未初始化的内存导致错误

    // 配置交换链参数
    sd.BufferCount = 2;                   // 缓冲区数量，2表示双缓冲
    sd.BufferDesc.Width = 0;              // 缓冲区宽度，0表示自动匹配窗口宽度
    sd.BufferDesc.Height = 0;             // 缓冲区高度，0表示自动匹配窗口高度
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式，32位RGBA（8位/通道）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子，60表示60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母，60/1=60Hz
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（窗口/全屏）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途，作为渲染目标
    sd.OutputWindow = hWnd;               // 绑定的窗口，渲染结果显示到该窗口
    sd.SampleDesc.Count = 1;              // 多重采样数量，1表示无抗锯齿
    sd.SampleDesc.Quality = 0;            // 采样质量，0表示默认
    sd.Windowed = TRUE;                   // 窗口模式，TRUE表示窗口化，FALSE表示全屏
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果，交换后丢弃后台缓冲区数据

    UINT createDeviceFlags = 0;  // 创建设备的标志
    // 调试模式开关，需要安装DirectX SDK才能使用
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的Direct3D特性级别（版本）
    // 支持的Direct3D版本列表，优先使用11.0，不支持则使用10.0
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_0
    };

    // 创建设备、设备上下文和交换链
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr,                       // 显卡适配器，nullptr表示使用默认显卡
        D3D_DRIVER_TYPE_HARDWARE,      // 驱动类型，硬件加速（使用GPU）
        nullptr,                       // 软件渲染模块，不需要则为nullptr
        createDeviceFlags,             // 创建设备的标志
        featureLevelArray,             // 支持的Direct3D版本列表
        2,                             // 版本列表的数量
        D3D11_SDK_VERSION,             // SDK版本，使用当前版本
        &sd,                           // 交换链描述结构体
        &g_pSwapChain,                 // 输出参数，接收创建的交换链
        &g_pd3dDevice,                 // 输出参数，接收创建的D3D设备
        &featureLevel,                 // 输出参数，接收实际支持的Direct3D版本
        &g_pd3dDeviceContext           // 输出参数，接收创建的设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试使用软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,  // 软件渲染驱动
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 如果创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象
// 按照依赖顺序释放，避免资源引用冲突
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标视图

    // 释放交换链
    if (g_pSwapChain)
    {
        g_pSwapChain->Release();
        g_pSwapChain = nullptr;
    }
    // 释放设备上下文
    if (g_pd3dDeviceContext)
    {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = nullptr;
    }
    // 释放D3D设备
    if (g_pd3dDevice)
    {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
    }
}

// 主函数：程序入口点，控制整个程序的生命周期
int main() {
    // DPI适配：解决高分辨率屏幕下UI模糊的问题
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知

    // 获取主显示器的DPI缩放比例
    // MonitorFromPoint获取主显示器的句柄
    // ImGui_ImplWin32_GetDpiScaleForMonitor计算该显示器的缩放比例
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)
    );

    // 创建Windows窗口：ImGui需要一个窗口作为载体来显示UI
    // 定义窗口类结构，描述窗口的基本属性
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格，使用专属设备上下文
        WndProc,                     // 窗口消息处理函数
        0L, 0L,                      // 额外的类数据和窗口数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景画刷等（使用默认）
        L"ImGui Example",            // 窗口类名，用于标识该窗口类
        nullptr                      // 小图标（使用默认）
    };
    ::RegisterClassExW(&wc);  // 向系统注册窗口类

    // 创建窗口
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名，必须与注册的类名一致
        L"Dear ImGui DirectX11 Example",  // 窗口标题栏显示的文本
        WS_OVERLAPPEDWINDOW,         // 窗口风格，标准可调整大小的窗口
        100, 100,                    // 窗口初始位置（屏幕左上角坐标）
        (int)(1280 * main_scale),    // 窗口宽度，根据DPI缩放
        (int)(800 * main_scale),     // 窗口高度，根据DPI缩放
        nullptr, nullptr,            // 父窗口句柄和菜单句柄（无）
        wc.hInstance, nullptr        // 程序实例句柄和额外数据（无）
    );

    // 初始化DirectX 11渲染环境
    if (!CreateDeviceD3D(hwnd))  // 如果创建失败
    {
        CleanupDeviceD3D();  // 清理已创建的资源
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);  // 注销窗口类
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后窗口默认是隐藏的）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保窗口立即显示

    // 初始化ImGui：创建UI上下文和配置
    IMGUI_CHECKVERSION();  // 检查ImGui版本，确保编译版本与运行时版本一致
    ImGui::CreateContext(); // 创建ImGui上下文，管理UI状态和资源
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象，管理输入输出

    // 配置ImGui功能
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab等）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启游戏手柄导航

    // 设置UI缩放：适配高DPI屏幕，避免UI元素过小
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素的大小
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // 初始化ImGui后端：连接ImGui与系统和渲染API
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端，处理窗口消息和输入
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端，负责渲染UI

    // 程序状态变量：控制UI显示和存储用户输入数据
    bool show_demo_window = true;    // 是否显示ImGui演示窗口（未使用）
    bool show_another_window = false; // 是否显示另一个窗口（未使用）
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);       // 用于按钮颜色的变量

    // 输入框缓冲区：存储用户输入的文本
    char name[1024] = "";    // 用户名输入缓冲区，容量1024字节
    char pass[1024] = "";    // 密码输入缓冲区，容量1024字节
    char text[1024] = "";    // 备用文本缓冲区（未使用）

    // 多行输入框配置
    const size_t BUF_SIZE = 1024;                // 缓冲区最大容量
    char input_text[BUF_SIZE] = "1111...\n22222\n333";  // 初始文本内容

    // 主循环：程序的核心，持续运行直到用户关闭窗口
    bool done = false;  // 控制循环是否结束的标志
    while (!done)
    {
        // 处理窗口消息：从消息队列中获取并处理所有待处理消息
        MSG msg;
        // PeekMessage非阻塞地获取消息，PM_REMOVE表示获取后从队列中移除
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如将键盘扫描码转换为字符）
            ::DispatchMessage(&msg);   // 将消息分发到窗口的消息处理函数（WndProc）
            if (msg.message == WM_QUIT)  // 如果收到退出消息
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出主循环

        // 处理窗口遮挡：如果窗口被完全遮挡，减少渲染频率以节省资源
        if (g_SwapChainOccluded &&
            g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10毫秒
            continue;     // 跳过本次循环，不进行渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // 处理窗口大小调整：当窗口大小改变时，调整渲染目标
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标

            // 调整交换链缓冲区大小以匹配新的窗口尺寸
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight,
                DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标

        }

        // 开始ImGui新帧：准备绘制UI
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧（处理输入）
        ImGui::NewFrame();          // ImGui核心准备，开始定义UI

        // 定义UI界面：创建一个名为"我的IMGui"的窗口
        bool is_window_open = true;  // 控制窗口是否显示的标志
        // ImGui::Begin()参数说明：
        // - 第一个参数：窗口标题，同时作为窗口的唯一标识
        // - 第二个参数：控制窗口是否显示的指针，关闭窗口时会设为false
        // - 第三个参数：窗口标志（默认为0，使用默认窗口样式）
        ImGui::Begin("我的IMGui", &is_window_open);

        // 显示自动换行的长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        // 显示带颜色的文本
        // ImGui::TextColored()参数：
        // - 第一个参数：ImVec4类型的颜色（RGBA，每个分量0.0f-1.0f）
        // - 后续参数：格式化字符串和参数（与printf类似）
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");  // 粉色文本
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");  // 黄色文本

        // 显示带颜色的文本和帮助标记，并在同一行
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();  // 让下一个控件与当前控件在同一行
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        HelpMarker("52am");  // 显示帮助标记，鼠标悬停显示"52am"

        // 颜色编辑控件：允许用户选择颜色
        // ImGui::ColorEdit3()参数：
        // - 第一个参数：控件标签
        // - 第二个参数：颜色变量的指针（需要转换为float*）
        // 选择的颜色会存储到seBan变量中
        ImGui::ColorEdit3("clear color", (float*)&seBan);

        // 修改按钮样式：临时改变按钮在不同状态下的颜色
        // ImGui::PushStyleColor()参数：
        // - 第一个参数：要修改的颜色类型（ImGuiCol_开头的枚举）
        // - 第二个参数：新的颜色值（ImVec4类型）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);           // 按钮正常状态颜色
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f,1.0f }); // 鼠标悬停状态
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f,1.0f });  // 鼠标点击状态

        // 创建按钮：ImGui::Button()返回bool值，表示按钮是否被点击
        if (ImGui::Button("anNiu")) {
            // 按钮被点击时，显示黄色文本"dianjianniu"
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        // 恢复样式：弹出之前压入的3个颜色设置
        // 必须与PushStyleColor的数量一致，否则会影响其他UI元素
        ImGui::PopStyleColor(3);

        // 复选框：允许用户切换选项的开关状态
        // ImGui::Checkbox()参数：
        // - 第一个参数：复选框标签
        // - 第二个参数：bool变量的指针，存储复选框的状态（true=勾选，false=未勾选）
        static bool check = true;
        static bool check1 = true;
        static bool check2 = false;
        static bool check3 = true;
        ImGui::Checkbox("checkbox", &check);
        ImGui::Checkbox("checkbox1", &check1);
        ImGui::Checkbox("checkbox2", &check2);
        ImGui::Checkbox("checkbox3", &check3);

        // 单选框：从多个选项中选择一个
        // ImGui::RadioButton()参数：
        // - 第一个参数：单选框标签
        // - 第二个参数：当前选中项的索引指针
        // - 第三个参数：当前单选框的索引值
        static int radio_selected = 0;  // 存储选中项的索引
        ImGui::RadioButton("radio a", &radio_selected, 0); ImGui::SameLine();
        ImGui::RadioButton("radio b", &radio_selected, 1); ImGui::SameLine();
        ImGui::RadioButton("radio c", &radio_selected, 2);

        // 输入框：接收用户文本输入
        ImGui::Text("name");  // 显示"name"作为输入框的标签
        ImGui::SameLine();    // 与输入框在同一行

        // ImGui输入框的标识规则详解：
        // 1. 格式为"标签##标识符"：显示"标签"，但内部用"标识符"区分不同控件
        // 2. 格式为"##标识符"：不显示标签，仅用"标识符"作为内部标识
        // 3. 无"##"：整个字符串既作为显示标签，也作为内部标识
        // 这里"##name"表示：不显示标签，内部用"name"作为标识
        ImGui::InputText("##name", name, IM_ARRAYSIZE(name));

        ImGui::Text("pass");  // 显示"pass"作为密码框的标签
        ImGui::SameLine();
        // 密码输入框：ImGuiInputTextFlags_Password标志使输入内容显示为*
        ImGui::InputText("##pass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);
        ImGui::InputText("p2ass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);

        // 带提示的输入框：当输入框为空时显示提示文本
        char hint_text[1024] = "mo ren ti shi";  // 提示文本
        ImGui::InputTextWithHint("##InputTextWithHint", hint_text,
            name, IM_ARRAYSIZE(name));

        // 多行输入框：允许输入多行文本
        ImGui::InputTextMultiline(
            "##MultiLineInput",  // 内部标识（不显示标签）
            input_text,          // 存储文本的缓冲区
            BUF_SIZE,            // 缓冲区最大容量
            ImVec2(0, 200)       // 输入框尺寸（宽度0表示自适应窗口，高度200像素）
        );

        // 加static让f变成静态变量，静态变量在函数中只会执行一次
        // 第一次执行当前函数会执行 static float f = 0.0f; 这一行代码，第二次执行当前函数时会跳过 static float f = 0.0f;这一行代码
        // 这样就能修改f的值后不会被重新赋值成0了
        static float f = 0.0f;
        // 滑块
        ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
        ImGui::SliderFloat("##float", &f, 0.0f, 1.0f);

        ImGui::End();  // 结束窗口定义（必须与ImGui::Begin配对使用）

        // 渲染UI：将定义的UI绘制到屏幕上
        ImGui::Render();  // 生成绘制命令列表

        // 计算背景色（考虑透明度）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标：告诉GPU接下来的渲染输出到主渲染目标
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空渲染目标：用背景色填充屏幕，清除上一帧的内容
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView,
            clear_color_with_alpha);
        // 渲染ImGui的UI：执行绘制命令
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // 显示画面：交换前后缓冲区，将渲染好的画面显示到屏幕上
        // Present()参数：
        // - 第一个参数：1表示开启垂直同步（VSync），0表示关闭
        // - 第二个参数：交换标志（0表示默认行为）
        HRESULT hr = g_pSwapChain->Present(1, 0);  // 开启垂直同步
        // 检查交换链是否被遮挡，用于下一次循环的优化
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // 程序退出：清理所有资源
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 10. 10.ImGui-进度条

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151369500
- Description: æç« æµè§éè¯»504æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui å è½½è¿åº¦æ¡

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：9.ImGui-滑块 
进度条在下图红框位置 
 
然后在源码中找它，搜索Progress Bar 
 
复制到我们的代码中

```text
 // progress当前进度，progress_dir进度范围
 static float progress = 0.0f, progress_dir = 1.0f;
 progress += progress_dir * 0.4f * ImGui::GetIO().DeltaTime;
 // 第一个参数传当前进度，一个小数，第二个参数是进度条的长和高，第三个参数进度条里的描述
 ImGui::ProgressBar(progress, ImVec2(0.0f, 0.0f), "jinduxinxi");
 ImGui::ProgressBar(progress, ImVec2(300.0f, 20.0f));
 ImGui::SameLine(0.0f, ImGui::GetStyle().ItemInnerSpacing.x);
 ImGui::Text("Progress Bar");

```
 
完整代码

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：9.ImGui-滑块 
进度条在下图红框位置 
 
然后在源码中找它，搜索Progress Bar 
 
复制到我们的代码中 
 

```text
 // progress当前进度，progress_dir进度范围
 static float progress = 0.0f, progress_dir = 1.0f;
 progress += progress_dir * 0.4f * ImGui::GetIO().DeltaTime;
 // 第一个参数传当前进度，一个小数，第二个参数是进度条的长和高，第三个参数进度条里的描述
 ImGui::ProgressBar(progress, ImVec2(0.0f, 0.0f), "jinduxinxi");
 ImGui::ProgressBar(progress, ImVec2(300.0f, 20.0f));
 ImGui::SameLine(0.0f, ImGui::GetStyle().ItemInnerSpacing.x);
 ImGui::Text("Progress Bar");

```
 
完整代码 

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

// 声明ImGui的Win32消息处理函数（定义在imgui_impl_win32.cpp中）
// 该函数用于让ImGui处理鼠标、键盘等输入消息
// 参数说明：
// - hWnd: 窗口句柄，标识接收消息的窗口
// - msg: 消息类型，如WM_MOUSEMOVE（鼠标移动）、WM_KEYDOWN（按键按下）等
// - wParam: 消息参数1，存储与消息相关的附加信息
// - lParam: 消息参数2，存储与消息相关的附加信息
// 返回值：如果消息被ImGui处理则返回true，否则返回false
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 自定义辅助函数：创建带提示的帮助标记
// 当鼠标悬停在"(?)"上时，会显示提示文本
// 参数：
// - desc: 要显示的提示文本内容
static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");  // 显示灰色的"(?)"作为帮助标记
    // 检查鼠标是否悬停在当前项目上，并开始绘制提示框
    if (ImGui::BeginItemTooltip())
    {
        // 设置文本自动换行的宽度（为字体大小的35倍）
        // 避免提示文本过长导致超出窗口范围
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);  // 显示提示文本（无格式）
        ImGui::PopTextWrapPos();       // 恢复文本换行设置
        ImGui::EndTooltip();           // 结束提示框绘制
    }
}

// 窗口消息处理函数：处理所有与窗口相关的事件
// 包括窗口大小改变、关闭、鼠标键盘输入等
// 参数说明：
// - hWnd: 窗口句柄，标识当前接收消息的窗口
// - msg: 消息类型，Windows系统定义的消息编号
// - wParam: 消息参数1，具体含义取决于消息类型
// - lParam: 消息参数2，具体含义取决于消息类型
// 返回值：LRESULT类型，消息处理的结果
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息，优先处理UI相关的输入事件
    // 如果ImGui处理了该消息（如点击UI控件），则直接返回
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 根据消息类型进行不同处理
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        // 如果是窗口最小化，则不需要调整渲染资源
        if (wParam == SIZE_MINIMIZED)
            return 0;
        // 从lParam中提取新的窗口宽度和高度
        // LOWORD宏获取lParam的低16位，存储宽度
        // HIWORD宏获取lParam的高16位，存储高度
        g_ResizeWidth = (UINT)LOWORD(lParam);
        g_ResizeHeight = (UINT)HIWORD(lParam);
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单，避免菜单弹出时遮挡ImGui控件
        // SC_KEYMENU是系统菜单命令，0xfff0用于屏蔽低位的扩展信息
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标
// 渲染目标视图是GPU可以写入的资源视图
// 所有的渲染命令最终都会绘制到该渲染目标上
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时指针，用于获取后台缓冲区

    // 从交换链中获取后台缓冲区
    // 参数1：0表示获取第一个缓冲区（交换链通常有2个缓冲区）
    // 参数2：IID_ID3D11Texture2D是要获取的接口ID
    // 参数3：输出参数，接收后台缓冲区的指针
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    // 使用D3D设备创建渲染目标视图
    // 参数1：要绑定为渲染目标的纹理（这里是后台缓冲区）
    // 参数2：渲染目标视图的描述（nullptr表示使用默认设置）
    // 参数3：输出参数，接收创建的渲染目标视图
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);

    // 释放临时的后台缓冲区指针
    // 渲染目标视图已经引用了该缓冲区，不需要再保留此指针
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
// COM对象需要通过Release()方法释放，减少引用计数
// 当引用计数为0时，对象会被自动销毁
void CleanupRenderTarget()
{
    if (g_mainRenderTargetView)
    {
        g_mainRenderTargetView->Release();  // 释放渲染目标视图
        g_mainRenderTargetView = nullptr;   // 置空指针，避免野指针
    }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：
// - hWnd: 窗口句柄，渲染结果将显示在该窗口中
// 返回值：bool类型，true表示创建成功，false表示失败
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述结构体，定义交换链的属性
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免未初始化的内存导致错误

    // 配置交换链参数
    sd.BufferCount = 2;                   // 缓冲区数量，2表示双缓冲
    sd.BufferDesc.Width = 0;              // 缓冲区宽度，0表示自动匹配窗口宽度
    sd.BufferDesc.Height = 0;             // 缓冲区高度，0表示自动匹配窗口高度
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式，32位RGBA（8位/通道）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子，60表示60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母，60/1=60Hz
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（窗口/全屏）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途，作为渲染目标
    sd.OutputWindow = hWnd;               // 绑定的窗口，渲染结果显示到该窗口
    sd.SampleDesc.Count = 1;              // 多重采样数量，1表示无抗锯齿
    sd.SampleDesc.Quality = 0;            // 采样质量，0表示默认
    sd.Windowed = TRUE;                   // 窗口模式，TRUE表示窗口化，FALSE表示全屏
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果，交换后丢弃后台缓冲区数据

    UINT createDeviceFlags = 0;  // 创建设备的标志
    // 调试模式开关，需要安装DirectX SDK才能使用
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的Direct3D特性级别（版本）
    // 支持的Direct3D版本列表，优先使用11.0，不支持则使用10.0
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_0
    };

    // 创建设备、设备上下文和交换链
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr,                       // 显卡适配器，nullptr表示使用默认显卡
        D3D_DRIVER_TYPE_HARDWARE,      // 驱动类型，硬件加速（使用GPU）
        nullptr,                       // 软件渲染模块，不需要则为nullptr
        createDeviceFlags,             // 创建设备的标志
        featureLevelArray,             // 支持的Direct3D版本列表
        2,                             // 版本列表的数量
        D3D11_SDK_VERSION,             // SDK版本，使用当前版本
        &sd,                           // 交换链描述结构体
        &g_pSwapChain,                 // 输出参数，接收创建的交换链
        &g_pd3dDevice,                 // 输出参数，接收创建的D3D设备
        &featureLevel,                 // 输出参数，接收实际支持的Direct3D版本
        &g_pd3dDeviceContext           // 输出参数，接收创建的设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试使用软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,  // 软件渲染驱动
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 如果创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象
// 按照依赖顺序释放，避免资源引用冲突
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标视图

    // 释放交换链
    if (g_pSwapChain)
    {
        g_pSwapChain->Release();
        g_pSwapChain = nullptr;
    }
    // 释放设备上下文
    if (g_pd3dDeviceContext)
    {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = nullptr;
    }
    // 释放D3D设备
    if (g_pd3dDevice)
    {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
    }
}

// 主函数：程序入口点，控制整个程序的生命周期
int main() {
    // DPI适配：解决高分辨率屏幕下UI模糊的问题
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知

    // 获取主显示器的DPI缩放比例
    // MonitorFromPoint获取主显示器的句柄
    // ImGui_ImplWin32_GetDpiScaleForMonitor计算该显示器的缩放比例
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)
    );

    // 创建Windows窗口：ImGui需要一个窗口作为载体来显示UI
    // 定义窗口类结构，描述窗口的基本属性
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格，使用专属设备上下文
        WndProc,                     // 窗口消息处理函数
        0L, 0L,                      // 额外的类数据和窗口数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景画刷等（使用默认）
        L"ImGui Example",            // 窗口类名，用于标识该窗口类
        nullptr                      // 小图标（使用默认）
    };
    ::RegisterClassExW(&wc);  // 向系统注册窗口类

    // 创建窗口
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名，必须与注册的类名一致
        L"Dear ImGui DirectX11 Example",  // 窗口标题栏显示的文本
        WS_OVERLAPPEDWINDOW,         // 窗口风格，标准可调整大小的窗口
        100, 100,                    // 窗口初始位置（屏幕左上角坐标）
        (int)(1280 * main_scale),    // 窗口宽度，根据DPI缩放
        (int)(800 * main_scale),     // 窗口高度，根据DPI缩放
        nullptr, nullptr,            // 父窗口句柄和菜单句柄（无）
        wc.hInstance, nullptr        // 程序实例句柄和额外数据（无）
    );

    // 初始化DirectX 11渲染环境
    if (!CreateDeviceD3D(hwnd))  // 如果创建失败
    {
        CleanupDeviceD3D();  // 清理已创建的资源
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);  // 注销窗口类
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后窗口默认是隐藏的）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保窗口立即显示

    // 初始化ImGui：创建UI上下文和配置
    IMGUI_CHECKVERSION();  // 检查ImGui版本，确保编译版本与运行时版本一致
    ImGui::CreateContext(); // 创建ImGui上下文，管理UI状态和资源
    ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象，管理输入输出

    // 配置ImGui功能
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab等）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启游戏手柄导航

    // 设置UI缩放：适配高DPI屏幕，避免UI元素过小
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素的大小
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // 初始化ImGui后端：连接ImGui与系统和渲染API
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端，处理窗口消息和输入
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端，负责渲染UI

    // 程序状态变量：控制UI显示和存储用户输入数据
    bool show_demo_window = true;    // 是否显示ImGui演示窗口（未使用）
    bool show_another_window = false; // 是否显示另一个窗口（未使用）
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);       // 用于按钮颜色的变量

    // 输入框缓冲区：存储用户输入的文本
    char name[1024] = "";    // 用户名输入缓冲区，容量1024字节
    char pass[1024] = "";    // 密码输入缓冲区，容量1024字节
    char text[1024] = "";    // 备用文本缓冲区（未使用）

    // 多行输入框配置
    const size_t BUF_SIZE = 1024;                // 缓冲区最大容量
    char input_text[BUF_SIZE] = "1111...\n22222\n333";  // 初始文本内容

    // 主循环：程序的核心，持续运行直到用户关闭窗口
    bool done = false;  // 控制循环是否结束的标志
    while (!done)
    {
        // 处理窗口消息：从消息队列中获取并处理所有待处理消息
        MSG msg;
        // PeekMessage非阻塞地获取消息，PM_REMOVE表示获取后从队列中移除
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如将键盘扫描码转换为字符）
            ::DispatchMessage(&msg);   // 将消息分发到窗口的消息处理函数（WndProc）
            if (msg.message == WM_QUIT)  // 如果收到退出消息
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出主循环

        // 处理窗口遮挡：如果窗口被完全遮挡，减少渲染频率以节省资源
        if (g_SwapChainOccluded &&
            g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10毫秒
            continue;     // 跳过本次循环，不进行渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // 处理窗口大小调整：当窗口大小改变时，调整渲染目标
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标

            // 调整交换链缓冲区大小以匹配新的窗口尺寸
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight,
                DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标

        }

        // 开始ImGui新帧：准备绘制UI
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧（处理输入）
        ImGui::NewFrame();          // ImGui核心准备，开始定义UI

        // 定义UI界面：创建一个名为"我的IMGui"的窗口
        bool is_window_open = true;  // 控制窗口是否显示的标志
        // ImGui::Begin()参数说明：
        // - 第一个参数：窗口标题，同时作为窗口的唯一标识
        // - 第二个参数：控制窗口是否显示的指针，关闭窗口时会设为false
        // - 第三个参数：窗口标志（默认为0，使用默认窗口样式）
        ImGui::Begin("我的IMGui", &is_window_open);

        // 显示自动换行的长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        // 显示带颜色的文本
        // ImGui::TextColored()参数：
        // - 第一个参数：ImVec4类型的颜色（RGBA，每个分量0.0f-1.0f）
        // - 后续参数：格式化字符串和参数（与printf类似）
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink");  // 粉色文本
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");  // 黄色文本

        // 显示带颜色的文本和帮助标记，并在同一行
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();  // 让下一个控件与当前控件在同一行
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        HelpMarker("52am");  // 显示帮助标记，鼠标悬停显示"52am"

        // 颜色编辑控件：允许用户选择颜色
        // ImGui::ColorEdit3()参数：
        // - 第一个参数：控件标签
        // - 第二个参数：颜色变量的指针（需要转换为float*）
        // 选择的颜色会存储到seBan变量中
        ImGui::ColorEdit3("clear color", (float*)&seBan);

        // 修改按钮样式：临时改变按钮在不同状态下的颜色
        // ImGui::PushStyleColor()参数：
        // - 第一个参数：要修改的颜色类型（ImGuiCol_开头的枚举）
        // - 第二个参数：新的颜色值（ImVec4类型）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);           // 按钮正常状态颜色
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f,1.0f }); // 鼠标悬停状态
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f,1.0f });  // 鼠标点击状态

        // 创建按钮：ImGui::Button()返回bool值，表示按钮是否被点击
        if (ImGui::Button("anNiu")) {
            // 按钮被点击时，显示黄色文本"dianjianniu"
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        // 恢复样式：弹出之前压入的3个颜色设置
        // 必须与PushStyleColor的数量一致，否则会影响其他UI元素
        ImGui::PopStyleColor(3);

        // 复选框：允许用户切换选项的开关状态
        // ImGui::Checkbox()参数：
        // - 第一个参数：复选框标签
        // - 第二个参数：bool变量的指针，存储复选框的状态（true=勾选，false=未勾选）
        static bool check = true;
        static bool check1 = true;
        static bool check2 = false;
        static bool check3 = true;
        ImGui::Checkbox("checkbox", &check);
        ImGui::Checkbox("checkbox1", &check1);
        ImGui::Checkbox("checkbox2", &check2);
        ImGui::Checkbox("checkbox3", &check3);

        // 单选框：从多个选项中选择一个
        // ImGui::RadioButton()参数：
        // - 第一个参数：单选框标签
        // - 第二个参数：当前选中项的索引指针
        // - 第三个参数：当前单选框的索引值
        static int radio_selected = 0;  // 存储选中项的索引
        ImGui::RadioButton("radio a", &radio_selected, 0); ImGui::SameLine();
        ImGui::RadioButton("radio b", &radio_selected, 1); ImGui::SameLine();
        ImGui::RadioButton("radio c", &radio_selected, 2);

        // 输入框：接收用户文本输入
        ImGui::Text("name");  // 显示"name"作为输入框的标签
        ImGui::SameLine();    // 与输入框在同一行

        // ImGui输入框的标识规则详解：
        // 1. 格式为"标签##标识符"：显示"标签"，但内部用"标识符"区分不同控件
        // 2. 格式为"##标识符"：不显示标签，仅用"标识符"作为内部标识
        // 3. 无"##"：整个字符串既作为显示标签，也作为内部标识
        // 这里"##name"表示：不显示标签，内部用"name"作为标识
        ImGui::InputText("##name", name, IM_ARRAYSIZE(name));

        ImGui::Text("pass");  // 显示"pass"作为密码框的标签
        ImGui::SameLine();
        // 密码输入框：ImGuiInputTextFlags_Password标志使输入内容显示为*
        ImGui::InputText("##pass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);
        ImGui::InputText("p2ass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);

        // 带提示的输入框：当输入框为空时显示提示文本
        char hint_text[1024] = "mo ren ti shi";  // 提示文本
        ImGui::InputTextWithHint("##InputTextWithHint", hint_text,
            name, IM_ARRAYSIZE(name));

        // 多行输入框：允许输入多行文本
        ImGui::InputTextMultiline(
            "##MultiLineInput",  // 内部标识（不显示标签）
            input_text,          // 存储文本的缓冲区
            BUF_SIZE,            // 缓冲区最大容量
            ImVec2(0, 200)       // 输入框尺寸（宽度0表示自适应窗口，高度200像素）
        );

        // 加static让f变成静态变量，静态变量在函数中只会执行一次
        // 第一次执行当前函数会执行 static float f = 0.0f; 这一行代码，第二次执行当前函数时会跳过 static float f = 0.0f;这一行代码
        // 这样就能修改f的值后不会被重新赋值成0了
        static float f = 0.0f;
        // 滑块
        ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
        ImGui::SliderFloat("##float", &f, 0.0f, 1.0f);

        // progress当前进度，progress_dir进度范围
        static float progress = 0.0f, progress_dir = 1.0f;
        progress += progress_dir * 0.4f * ImGui::GetIO().DeltaTime;
        // 第一个参数传当前进度，一个小数，第二个参数是进度条的长和高，第三个参数进度条里的描述
        ImGui::ProgressBar(progress, ImVec2(0.0f, 0.0f), "jinduxinxi");
        ImGui::ProgressBar(progress, ImVec2(300.0f, 20.0f));
        ImGui::SameLine(0.0f, ImGui::GetStyle().ItemInnerSpacing.x);
        ImGui::Text("Progress Bar");

        ImGui::End();  // 结束窗口定义（必须与ImGui::Begin配对使用）

        // 渲染UI：将定义的UI绘制到屏幕上
        ImGui::Render();  // 生成绘制命令列表

        // 计算背景色（考虑透明度）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标：告诉GPU接下来的渲染输出到主渲染目标
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空渲染目标：用背景色填充屏幕，清除上一帧的内容
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView,
            clear_color_with_alpha);
        // 渲染ImGui的UI：执行绘制命令
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // 显示画面：交换前后缓冲区，将渲染好的画面显示到屏幕上
        // Present()参数：
        // - 第一个参数：1表示开启垂直同步（VSync），0表示关闭
        // - 第二个参数：交换标志（0表示默认行为）
        HRESULT hr = g_pSwapChain->Present(1, 0);  // 开启垂直同步
        // 检查交换链是否被遮挡，用于下一次循环的优化
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // 程序退出：清理所有资源
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 11. 11.ImGui-加载字体和中文

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151410958
- Description: æç« æµè§éè¯»1.3kæ¬¡ï¼ç¹èµ18æ¬¡ï¼æ¶è5æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imguiå­ä½

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：10.ImGui-进度条 
如下图现在的中文是乱码的，这个原因是没有加载支持中文的字体 
 
加载字体的代码是

```text
ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象，管理输入输出
io.Fonts.xxx // xxx是加载字体的方式

```
 
如下图加载字体所有的方式，ttf是字体的文件类型 
 
下图红框就是一个字体文件，我使用的是在内存中加载字体的方式，这样比较快，怎么把文件搞成内存里的东西？ 
 
在ImGui源码文件中，也有很多字体文件，如下图红框 
 
下图红框的cpp是可以运行的，下图的cpp就可以把一个ttf文件搞成c++类，这样就能在内存中使用了 
 
打开vs2022，点击下图红框新建项目 
 
空项目 
 
然后点击在文件资源管理器中打开文件夹，打开它的文件目录 
 
把下图红框的cpp复制到刚刚创建的项目里 
 
再把它拖到vs2022里 
 
然后改成Release，然后重新生成 
 
然后找到重新生成之后的文件，也就是下图红框的ceshiziti.exe文件，然后把字体文件复制过来 
 
然后输入cmd按回车 
 
然后运行指令 ceshiziti.exe -nocompress Test.ttf front_data > front.h，这样就会把Test.ttf搞成C++代码 
 
front.h的内容 
 
然后把这个front.h文件复制到我们的项目里 
 
然后再把它拖到头文件里 
 
如下图 
 
然后引入这个front.h文件 
 
加载字体的代码

```text
 ImGuiIO& io = ImGui::GetIO();

// 创建字体配置结构体（ImFontConfig），用于自定义字体加载的各种参数
 // 该结构体包含字体大小、是否合并字体、字体数据所有权等配置项
 ImFontConfig ifc;

// 设置字体数据的所有权：false表示字体数据（front_data_data）不由ImGui的字体图集（FontAtlas）管理
 // 含义：ImGui不会自动释放front_data_data指向的内存，需要用户在程序结束时手动释放
 // 反之，若设为true，ImGui会在销毁字体图集时自动释放该内存（适用于临时加载的字体数据）
 ifc.FontDataOwnedByAtlas = false;

// 从内存中的TTF字体数据加载字体，并添加到字体图集中
 // 参数说明：
 // 1. (void*)front_data_data：指向内存中TTF字体文件数据的指针（二进制数据）
 // 2. front_data_size：TTF字体数据的大小（字节数），用于告诉ImGui需要读取多少数据
 // 3. 18.0f：字体的点大小（Point Size），是字体设计时的原始大小（与屏幕分辨率无关）
 // 4. &ifc：字体配置结构体指针，使用上面定义的自定义配置（如所有权设置）
 // 5. io.Fonts->GetGlyphRangesChineseFull()：指定需要加载的中文字符集范围
 //    GetGlyphRangesChineseFull()会返回包含大部分简体/繁体中文的字符范围，确保中文能正常显示
 // 返回值：ImFont* 指向加载成功的字体对象，后续可通过该指针切换UI使用的字体
 ImFont* front = io.Fonts->AddFontFromMemoryTTF(
     (void*)front_data_data,
     front_data_size,
     18.0f,
     &ifc,
     io.Fonts->GetGlyphRangesChineseFull()
 );

```
 
 
效果图：前面带u8 表示使用utf8编码，我们加载的字体也是用的utf8编码，一个没加一个加了，可以看得出来效果，没加的中文还是乱码，加了的中文正常显示 
 
完整代码：

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：10.ImGui-进度条 
如下图现在的中文是乱码的，这个原因是没有加载支持中文的字体 
 
加载字体的代码是 

```text
ImGuiIO& io = ImGui::GetIO(); (void)io;  // 获取IO对象，管理输入输出
io.Fonts.xxx // xxx是加载字体的方式

```
 
如下图加载字体所有的方式，ttf是字体的文件类型 
 
下图红框就是一个字体文件，我使用的是在内存中加载字体的方式，这样比较快，怎么把文件搞成内存里的东西？ 
 
在ImGui源码文件中，也有很多字体文件，如下图红框 
 
下图红框的cpp是可以运行的，下图的cpp就可以把一个ttf文件搞成c++类，这样就能在内存中使用了 
 
打开vs2022，点击下图红框新建项目 
 
空项目 
 
然后点击在文件资源管理器中打开文件夹，打开它的文件目录 
 
把下图红框的cpp复制到刚刚创建的项目里 
 
再把它拖到vs2022里 
 
然后改成Release，然后重新生成 
 
然后找到重新生成之后的文件，也就是下图红框的ceshiziti.exe文件，然后把字体文件复制过来 
 
然后输入cmd按回车 
 
然后运行指令 ceshiziti.exe -nocompress Test.ttf front_data > front.h，这样就会把Test.ttf搞成C++代码 
 
front.h的内容 
 
然后把这个front.h文件复制到我们的项目里 
 
然后再把它拖到头文件里 
 
如下图 
 
然后引入这个front.h文件 
 
加载字体的代码 

```text
 ImGuiIO& io = ImGui::GetIO();

 // 创建字体配置结构体（ImFontConfig），用于自定义字体加载的各种参数
 // 该结构体包含字体大小、是否合并字体、字体数据所有权等配置项
 ImFontConfig ifc;

 // 设置字体数据的所有权：false表示字体数据（front_data_data）不由ImGui的字体图集（FontAtlas）管理
 // 含义：ImGui不会自动释放front_data_data指向的内存，需要用户在程序结束时手动释放
 // 反之，若设为true，ImGui会在销毁字体图集时自动释放该内存（适用于临时加载的字体数据）
 ifc.FontDataOwnedByAtlas = false;

 // 从内存中的TTF字体数据加载字体，并添加到字体图集中
 // 参数说明：
 // 1. (void*)front_data_data：指向内存中TTF字体文件数据的指针（二进制数据）
 // 2. front_data_size：TTF字体数据的大小（字节数），用于告诉ImGui需要读取多少数据
 // 3. 18.0f：字体的点大小（Point Size），是字体设计时的原始大小（与屏幕分辨率无关）
 // 4. &ifc：字体配置结构体指针，使用上面定义的自定义配置（如所有权设置）
 // 5. io.Fonts->GetGlyphRangesChineseFull()：指定需要加载的中文字符集范围
 //    GetGlyphRangesChineseFull()会返回包含大部分简体/繁体中文的字符范围，确保中文能正常显示
 // 返回值：ImFont* 指向加载成功的字体对象，后续可通过该指针切换UI使用的字体
 ImFont* front = io.Fonts->AddFontFromMemoryTTF(
     (void*)front_data_data,
     front_data_size,
     18.0f,
     &ifc,
     io.Fonts->GetGlyphRangesChineseFull()
 );

```
 
 
效果图：前面带u8 表示使用utf8编码，我们加载的字体也是用的utf8编码，一个没加一个加了，可以看得出来效果，没加的中文还是乱码，加了的中文正常显示 
 
完整代码： 

```text
#include "main.h"  // 包含程序所需的头文件，其中声明了ImGui、DirectX等库的必要函数和类

// 全局变量：存储DirectX 11核心资源和窗口状态（整个程序共享）
static UINT                     g_ResizeWidth = 0, g_ResizeHeight = 0;
// 窗口调整大小时的新宽度和高度
// 当窗口大小改变时，WM_SIZE消息会将新尺寸存储到这两个变量中
// 主循环会检测这两个变量，当它们不为0时进行渲染目标的调整

static ID3D11Device* g_pd3dDevice = nullptr;
// Direct3D 11设备对象，是DirectX渲染的核心
// 负责创建所有的渲染资源，如纹理、缓冲区、渲染目标等
// 所有与硬件交互的渲染资源创建都需要通过该设备对象

static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr;
// Direct3D 11设备上下文，相当于渲染命令的执行者
// 用于设置渲染状态、绑定资源、执行绘制命令等操作
// 可以理解为向GPU发送渲染指令的接口

static IDXGISwapChain* g_pSwapChain = nullptr;
// 交换链对象，管理前后两个缓冲区实现双缓冲机制
// 前端缓冲区是正在显示的画面，后端缓冲区是正在渲染的画面
// 渲染完成后通过交换操作将后端缓冲区变为前端，避免画面闪烁

static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr;
// 主渲染目标视图，是交换链后端缓冲区的视图
// 告诉GPU渲染结果应该输出到哪个缓冲区
// ImGui绘制的所有UI最终都会渲染到这个目标上

static bool                     g_SwapChainOccluded = false;
// 标记交换链是否被遮挡（如窗口被其他窗口完全覆盖）
// 当为true时可以暂停渲染以节省CPU和GPU资源
// 由Present函数的返回值判断并设置

// 声明ImGui的Win32消息处理函数（定义在imgui_impl_win32.cpp中）
// 该函数用于让ImGui处理鼠标、键盘等输入消息
// 参数说明：
// - hWnd: 窗口句柄，标识接收消息的窗口
// - msg: 消息类型，如WM_MOUSEMOVE（鼠标移动）、WM_KEYDOWN（按键按下）等
// - wParam: 消息参数1，存储与消息相关的附加信息
// - lParam: 消息参数2，存储与消息相关的附加信息
// 返回值：如果消息被ImGui处理则返回true，否则返回false
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);

// 自定义辅助函数：创建带提示的帮助标记
// 当鼠标悬停在"(?)"上时，会显示提示文本
// 参数：
// - desc: 要显示的提示文本内容
static void HelpMarker(const char* desc)
{
    ImGui::TextDisabled("(?)");  // 显示灰色的"(?)"作为帮助标记
    // 检查鼠标是否悬停在当前项目上，并开始绘制提示框
    if (ImGui::BeginItemTooltip())
    {
        // 设置文本自动换行的宽度（为字体大小的35倍）
        // 避免提示文本过长导致超出窗口范围
        ImGui::PushTextWrapPos(ImGui::GetFontSize() * 35.0f);
        ImGui::TextUnformatted(desc);  // 显示提示文本（无格式）
        ImGui::PopTextWrapPos();       // 恢复文本换行设置
        ImGui::EndTooltip();           // 结束提示框绘制
    }
}

// 窗口消息处理函数：处理所有与窗口相关的事件
// 包括窗口大小改变、关闭、鼠标键盘输入等
// 参数说明：
// - hWnd: 窗口句柄，标识当前接收消息的窗口
// - msg: 消息类型，Windows系统定义的消息编号
// - wParam: 消息参数1，具体含义取决于消息类型
// - lParam: 消息参数2，具体含义取决于消息类型
// 返回值：LRESULT类型，消息处理的结果
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 让ImGui先处理消息，优先处理UI相关的输入事件
    // 如果ImGui处理了该消息（如点击UI控件），则直接返回
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 根据消息类型进行不同处理
    switch (msg)
    {
    case WM_SIZE:  // 窗口大小改变事件
        // 如果是窗口最小化，则不需要调整渲染资源
        if (wParam == SIZE_MINIMIZED)
            return 0;
        // 从lParam中提取新的窗口宽度和高度
        // LOWORD宏获取lParam的低16位，存储宽度
        // HIWORD宏获取lParam的高16位，存储高度
        g_ResizeWidth = (UINT)LOWORD(lParam);
        g_ResizeHeight = (UINT)HIWORD(lParam);
        return 0;

    case WM_SYSCOMMAND:  // 系统命令事件（如ALT+空格调出窗口菜单）
        // 禁用ALT菜单，避免菜单弹出时遮挡ImGui控件
        // SC_KEYMENU是系统菜单命令，0xfff0用于屏蔽低位的扩展信息
        if ((wParam & 0xfff0) == SC_KEYMENU)
            return 0;
        break;  // 其他系统命令交给默认处理

    case WM_DESTROY:  // 窗口销毁事件（如点击关闭按钮）
        ::PostQuitMessage(0);  // 发送退出消息，主循环会捕获并结束程序
        return 0;
    }

    // 其他未处理的消息，交给Windows系统默认处理
    return ::DefWindowProcW(hWnd, msg, wParam, lParam);
}

// 创建渲染目标视图：将交换链的后台缓冲区绑定为渲染目标
// 渲染目标视图是GPU可以写入的资源视图
// 所有的渲染命令最终都会绘制到该渲染目标上
void CreateRenderTarget()
{
    ID3D11Texture2D* pBackBuffer = nullptr;  // 临时指针，用于获取后台缓冲区

    // 从交换链中获取后台缓冲区
    // 参数1：0表示获取第一个缓冲区（交换链通常有2个缓冲区）
    // 参数2：IID_ID3D11Texture2D是要获取的接口ID
    // 参数3：输出参数，接收后台缓冲区的指针
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));

    // 使用D3D设备创建渲染目标视图
    // 参数1：要绑定为渲染目标的纹理（这里是后台缓冲区）
    // 参数2：渲染目标视图的描述（nullptr表示使用默认设置）
    // 参数3：输出参数，接收创建的渲染目标视图
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);

    // 释放临时的后台缓冲区指针
    // 渲染目标视图已经引用了该缓冲区，不需要再保留此指针
    pBackBuffer->Release();
}

// 清理渲染目标视图：释放资源，避免内存泄漏
// COM对象需要通过Release()方法释放，减少引用计数
// 当引用计数为0时，对象会被自动销毁
void CleanupRenderTarget()
{
    if (g_mainRenderTargetView)
    {
        g_mainRenderTargetView->Release();  // 释放渲染目标视图
        g_mainRenderTargetView = nullptr;   // 置空指针，避免野指针
    }
}

// 创建D3D11设备和交换链：初始化DirectX渲染环境
// 参数：
// - hWnd: 窗口句柄，渲染结果将显示在该窗口中
// 返回值：bool类型，true表示创建成功，false表示失败
bool CreateDeviceD3D(HWND hWnd)
{
    // 初始化交换链描述结构体，定义交换链的属性
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免未初始化的内存导致错误

    // 配置交换链参数
    sd.BufferCount = 2;                   // 缓冲区数量，2表示双缓冲
    sd.BufferDesc.Width = 0;              // 缓冲区宽度，0表示自动匹配窗口宽度
    sd.BufferDesc.Height = 0;             // 缓冲区高度，0表示自动匹配窗口高度
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式，32位RGBA（8位/通道）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子，60表示60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母，60/1=60Hz
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（窗口/全屏）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途，作为渲染目标
    sd.OutputWindow = hWnd;               // 绑定的窗口，渲染结果显示到该窗口
    sd.SampleDesc.Count = 1;              // 多重采样数量，1表示无抗锯齿
    sd.SampleDesc.Quality = 0;            // 采样质量，0表示默认
    sd.Windowed = TRUE;                   // 窗口模式，TRUE表示窗口化，FALSE表示全屏
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果，交换后丢弃后台缓冲区数据

    UINT createDeviceFlags = 0;  // 创建设备的标志
    // 调试模式开关，需要安装DirectX SDK才能使用
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的Direct3D特性级别（版本）
    // 支持的Direct3D版本列表，优先使用11.0，不支持则使用10.0
    const D3D_FEATURE_LEVEL featureLevelArray[2] = {
        D3D_FEATURE_LEVEL_11_0,
        D3D_FEATURE_LEVEL_10_0
    };

    // 创建设备、设备上下文和交换链
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr,                       // 显卡适配器，nullptr表示使用默认显卡
        D3D_DRIVER_TYPE_HARDWARE,      // 驱动类型，硬件加速（使用GPU）
        nullptr,                       // 软件渲染模块，不需要则为nullptr
        createDeviceFlags,             // 创建设备的标志
        featureLevelArray,             // 支持的Direct3D版本列表
        2,                             // 版本列表的数量
        D3D11_SDK_VERSION,             // SDK版本，使用当前版本
        &sd,                           // 交换链描述结构体
        &g_pSwapChain,                 // 输出参数，接收创建的交换链
        &g_pd3dDevice,                 // 输出参数，接收创建的D3D设备
        &featureLevel,                 // 输出参数，接收实际支持的Direct3D版本
        &g_pd3dDeviceContext           // 输出参数，接收创建的设备上下文
    );

    // 如果硬件加速失败（如显卡不支持D3D11），尝试使用软件渲染（WARP驱动）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,  // 软件渲染驱动
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    if (res != S_OK)  // 如果创建失败（S_OK表示成功）
        return false;

    CreateRenderTarget();  // 创建渲染目标视图
    return true;
}

// 清理D3D资源：释放所有DirectX相关对象
// 按照依赖顺序释放，避免资源引用冲突
void CleanupDeviceD3D()
{
    CleanupRenderTarget();  // 先清理渲染目标视图

    // 释放交换链
    if (g_pSwapChain)
    {
        g_pSwapChain->Release();
        g_pSwapChain = nullptr;
    }
    // 释放设备上下文
    if (g_pd3dDeviceContext)
    {
        g_pd3dDeviceContext->Release();
        g_pd3dDeviceContext = nullptr;
    }
    // 释放D3D设备
    if (g_pd3dDevice)
    {
        g_pd3dDevice->Release();
        g_pd3dDevice = nullptr;
    }
}

// 主函数：程序入口点，控制整个程序的生命周期
int main() {
    // DPI适配：解决高分辨率屏幕下UI模糊的问题
    ImGui_ImplWin32_EnableDpiAwareness();  // 开启ImGui对系统DPI的感知

    // 获取主显示器的DPI缩放比例
    // MonitorFromPoint获取主显示器的句柄
    // ImGui_ImplWin32_GetDpiScaleForMonitor计算该显示器的缩放比例
    float main_scale = ImGui_ImplWin32_GetDpiScaleForMonitor(
        ::MonitorFromPoint(POINT{ 0, 0 }, MONITOR_DEFAULTTOPRIMARY)
    );

    // 创建Windows窗口：ImGui需要一个窗口作为载体来显示UI
    // 定义窗口类结构，描述窗口的基本属性
    WNDCLASSEXW wc = {
        sizeof(wc),                  // 结构体大小
        CS_CLASSDC,                  // 窗口类风格，使用专属设备上下文
        WndProc,                     // 窗口消息处理函数
        0L, 0L,                      // 额外的类数据和窗口数据（未使用）
        GetModuleHandle(nullptr),    // 程序实例句柄
        nullptr, nullptr, nullptr, nullptr,  // 图标、光标、背景画刷等（使用默认）
        L"ImGui Example",            // 窗口类名，用于标识该窗口类
        nullptr                      // 小图标（使用默认）
    };
    ::RegisterClassExW(&wc);  // 向系统注册窗口类

    // 创建窗口
    HWND hwnd = ::CreateWindowW(
        wc.lpszClassName,            // 窗口类名，必须与注册的类名一致
        L"Dear ImGui DirectX11 Example",  // 窗口标题栏显示的文本
        WS_OVERLAPPEDWINDOW,         // 窗口风格，标准可调整大小的窗口
        100, 100,                    // 窗口初始位置（屏幕左上角坐标）
        (int)(1280 * main_scale),    // 窗口宽度，根据DPI缩放
        (int)(800 * main_scale),     // 窗口高度，根据DPI缩放
        nullptr, nullptr,            // 父窗口句柄和菜单句柄（无）
        wc.hInstance, nullptr        // 程序实例句柄和额外数据（无）
    );

    // 初始化DirectX 11渲染环境
    if (!CreateDeviceD3D(hwnd))  // 如果创建失败
    {
        CleanupDeviceD3D();  // 清理已创建的资源
        ::UnregisterClassW(wc.lpszClassName, wc.hInstance);  // 注销窗口类
        return 1;  // 返回1表示程序异常退出
    }

    // 显示窗口（创建后窗口默认是隐藏的）
    ::ShowWindow(hwnd, SW_SHOWDEFAULT);
    ::UpdateWindow(hwnd);  // 刷新窗口，确保窗口立即显示

    // 初始化ImGui：创建UI上下文和配置
    IMGUI_CHECKVERSION();  // 检查ImGui版本，确保编译版本与运行时版本一致
    ImGui::CreateContext(); // 创建ImGui上下文，管理UI状态和资源
    // 获取ImGui的IO（输入输出）对象
// ImGuiIO是ImGui的核心配置对象，负责管理输入（鼠标、键盘、控制器）、输出（字体、显示尺寸等）
// 这里通过ImGui::GetIO()获取全局唯一的IO实例，后续字体配置需要通过它的Fonts成员（字体图集）进行
    ImGuiIO& io = ImGui::GetIO();

    // 创建字体配置结构体（ImFontConfig），用于自定义字体加载的各种参数
    // 该结构体包含字体大小、是否合并字体、字体数据所有权等配置项
    ImFontConfig ifc;

    // 设置字体数据的所有权：false表示字体数据（front_data_data）不由ImGui的字体图集（FontAtlas）管理
    // 含义：ImGui不会自动释放front_data_data指向的内存，需要用户在程序结束时手动释放
    // 反之，若设为true，ImGui会在销毁字体图集时自动释放该内存（适用于临时加载的字体数据）
    ifc.FontDataOwnedByAtlas = false;

    // 从内存中的TTF字体数据加载字体，并添加到字体图集中
    // 参数说明：
    // 1. (void*)front_data_data：指向内存中TTF字体文件数据的指针（二进制数据）
    // 2. front_data_size：TTF字体数据的大小（字节数），用于告诉ImGui需要读取多少数据
    // 3. 18.0f：字体的点大小（Point Size），是字体设计时的原始大小（与屏幕分辨率无关）
    // 4. &ifc：字体配置结构体指针，使用上面定义的自定义配置（如所有权设置）
    // 5. io.Fonts->GetGlyphRangesChineseFull()：指定需要加载的中文字符集范围
    //    GetGlyphRangesChineseFull()会返回包含大部分简体/繁体中文的字符范围，确保中文能正常显示
    // 返回值：ImFont* 指向加载成功的字体对象，后续可通过该指针切换UI使用的字体
    ImFont* front = io.Fonts->AddFontFromMemoryTTF(
        (void*)front_data_data,
        front_data_size,
        18.0f,
        &ifc,
        io.Fonts->GetGlyphRangesChineseFull()
    );

    // 配置ImGui功能
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // 开启键盘导航（方向键、Tab等）
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;   // 开启游戏手柄导航

    // 设置UI缩放：适配高DPI屏幕，避免UI元素过小
    ImGuiStyle& style = ImGui::GetStyle();
    style.ScaleAllSizes(main_scale);  // 缩放所有UI元素的大小
    style.FontScaleDpi = main_scale;  // 缩放字体大小

    // 初始化ImGui后端：连接ImGui与系统和渲染API
    ImGui_ImplWin32_Init(hwnd);       // 初始化Win32后端，处理窗口消息和输入
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);  // 初始化DX11后端，负责渲染UI

    // 程序状态变量：控制UI显示和存储用户输入数据
    bool show_demo_window = true;    // 是否显示ImGui演示窗口（未使用）
    bool show_another_window = false; // 是否显示另一个窗口（未使用）
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f); // 窗口背景色（浅蓝色）
    ImVec4 seBan = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);       // 用于按钮颜色的变量

    // 输入框缓冲区：存储用户输入的文本
    char name[1024] = "";    // 用户名输入缓冲区，容量1024字节
    char pass[1024] = "";    // 密码输入缓冲区，容量1024字节
    char text[1024] = "";    // 备用文本缓冲区（未使用）

    // 多行输入框配置
    const size_t BUF_SIZE = 1024;                // 缓冲区最大容量
    char input_text[BUF_SIZE] = "1111...\n22222\n333";  // 初始文本内容

    // 主循环：程序的核心，持续运行直到用户关闭窗口
    bool done = false;  // 控制循环是否结束的标志
    while (!done)
    {
        // 处理窗口消息：从消息队列中获取并处理所有待处理消息
        MSG msg;
        // PeekMessage非阻塞地获取消息，PM_REMOVE表示获取后从队列中移除
        while (::PeekMessage(&msg, nullptr, 0U, 0U, PM_REMOVE))
        {
            ::TranslateMessage(&msg);  // 翻译消息（如将键盘扫描码转换为字符）
            ::DispatchMessage(&msg);   // 将消息分发到窗口的消息处理函数（WndProc）
            if (msg.message == WM_QUIT)  // 如果收到退出消息
                done = true;  // 标记循环结束
        }
        if (done)
            break;  // 退出主循环

        // 处理窗口遮挡：如果窗口被完全遮挡，减少渲染频率以节省资源
        if (g_SwapChainOccluded &&
            g_pSwapChain->Present(0, DXGI_PRESENT_TEST) == DXGI_STATUS_OCCLUDED)
        {
            ::Sleep(10);  // 休眠10毫秒
            continue;     // 跳过本次循环，不进行渲染
        }
        g_SwapChainOccluded = false;  // 重置遮挡状态

        // 处理窗口大小调整：当窗口大小改变时，调整渲染目标
        if (g_ResizeWidth != 0 && g_ResizeHeight != 0)
        {
            CleanupRenderTarget();  // 先清理旧的渲染目标

            // 调整交换链缓冲区大小以匹配新的窗口尺寸
            g_pSwapChain->ResizeBuffers(0, g_ResizeWidth, g_ResizeHeight,
                DXGI_FORMAT_UNKNOWN, 0);
            g_ResizeWidth = g_ResizeHeight = 0;  // 重置尺寸变量
            CreateRenderTarget();  // 创建新的渲染目标

        }

        // 开始ImGui新帧：准备绘制UI
        ImGui_ImplDX11_NewFrame();  // DX11后端准备新帧
        ImGui_ImplWin32_NewFrame(); // Win32后端准备新帧（处理输入）
        ImGui::NewFrame();          // ImGui核心准备，开始定义UI

        // 定义UI界面：创建一个名为"我的IMGui"的窗口
        bool is_window_open = true;  // 控制窗口是否显示的标志
        // ImGui::Begin()参数说明：
        // - 第一个参数：窗口标题，同时作为窗口的唯一标识
        // - 第二个参数：控制窗口是否显示的指针，关闭窗口时会设为false
        // - 第三个参数：窗口标志（默认为0，使用默认窗口样式）
        // 带中文的字符前面要带着u8
      // 开始创建一个ImGui窗口，与ImGui::End()配对使用，中间的代码定义窗口内容
        // 函数作用：初始化窗口状态（位置、大小、标题等），并准备绘制窗口内的UI元素
        // 返回值：bool类型，若为true表示窗口处于激活状态（可绘制内容）；若为false表示窗口被最小化或关闭，此时应跳过绘制直接调用ImGui::End()
                ImGui::Begin(
                    u8"我的IMGui",  // 窗口标题（显示在标题栏），同时作为窗口的唯一标识
                    // u8前缀表示字符串采用UTF-8编码，确保中文"我的IMGui"能正确显示（避免乱码）
                    // 注意：不同窗口的标题需唯一，否则ImGui会视为同一个窗口
                    &is_window_open // 指向bool变量的指针，用于控制窗口是否显示
                    // 当用户点击窗口右上角的关闭按钮时，ImGui会自动将*is_window_open设为false
                    // 若传入nullptr，则窗口无法通过UI关闭（只能通过代码控制）
        // 可选参数（此处未使用）：窗口标志（如ImGuiWindowFlags_NoTitleBar去除标题栏等）
        );

        // 显示自动换行的长文本
        ImGui::TextWrapped(
            "This 521 "
            "aiamaiamaiamaiamaiamaiamaiamaiamaiamaiamaiam");

        // 显示带颜色的文本
        // ImGui::TextColored()参数：
        // - 第一个参数：ImVec4类型的颜色（RGBA，每个分量0.0f-1.0f）
        // - 后续参数：格式化字符串和参数（与printf类似）
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pin中文k");  // 粉色文本
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow");  // 黄色文本

        // 显示带颜色的文本和帮助标记，并在同一行
        ImGui::TextColored(ImVec4(1.0f, 0.0f, 1.0f, 1.0f), "Pink2");
        ImGui::SameLine();  // 让下一个控件与当前控件在同一行
        ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "Yellow2");
        ImGui::SameLine();
        HelpMarker("52am");  // 显示帮助标记，鼠标悬停显示"52am"

        // 颜色编辑控件：允许用户选择颜色
        // ImGui::ColorEdit3()参数：
        // - 第一个参数：控件标签
        // - 第二个参数：颜色变量的指针（需要转换为float*）
        // 选择的颜色会存储到seBan变量中
        ImGui::ColorEdit3("clear color", (float*)&seBan);

        // 修改按钮样式：临时改变按钮在不同状态下的颜色
        // ImGui::PushStyleColor()参数：
        // - 第一个参数：要修改的颜色类型（ImGuiCol_开头的枚举）
        // - 第二个参数：新的颜色值（ImVec4类型）
        ImGui::PushStyleColor(ImGuiCol_Button, seBan);           // 按钮正常状态颜色
        ImGui::PushStyleColor(ImGuiCol_ButtonHovered, { 1.0f,0.0f,0.0f,1.0f }); // 鼠标悬停状态
        ImGui::PushStyleColor(ImGuiCol_ButtonActive, { 0.0f,1.0f,0.0f,1.0f });  // 鼠标点击状态

        // 创建按钮：ImGui::Button()返回bool值，表示按钮是否被点击
        if (ImGui::Button("anNiu")) {
            // 按钮被点击时，显示黄色文本"dianjianniu"
            ImGui::TextColored(ImVec4(1.0f, 1.0f, 0.0f, 1.0f), "dianjianniu");
        }

        // 恢复样式：弹出之前压入的3个颜色设置
        // 必须与PushStyleColor的数量一致，否则会影响其他UI元素
        ImGui::PopStyleColor(3);

        // 复选框：允许用户切换选项的开关状态
        // ImGui::Checkbox()参数：
        // - 第一个参数：复选框标签
        // - 第二个参数：bool变量的指针，存储复选框的状态（true=勾选，false=未勾选）
        static bool check = true;
        static bool check1 = true;
        static bool check2 = false;
        static bool check3 = true;
        ImGui::Checkbox("checkbox", &check);
        ImGui::Checkbox("checkbox1", &check1);
        ImGui::Checkbox("checkbox2", &check2);
        ImGui::Checkbox("checkbox3", &check3);

        // 单选框：从多个选项中选择一个
        // ImGui::RadioButton()参数：
        // - 第一个参数：单选框标签
        // - 第二个参数：当前选中项的索引指针
        // - 第三个参数：当前单选框的索引值
        static int radio_selected = 0;  // 存储选中项的索引
        ImGui::RadioButton("radio a", &radio_selected, 0); ImGui::SameLine();
        ImGui::RadioButton("radio b", &radio_selected, 1); ImGui::SameLine();
        ImGui::RadioButton("radio c", &radio_selected, 2);

        // 输入框：接收用户文本输入
        ImGui::Text("name");  // 显示"name"作为输入框的标签
        ImGui::SameLine();    // 与输入框在同一行

        // ImGui输入框的标识规则详解：
        // 1. 格式为"标签##标识符"：显示"标签"，但内部用"标识符"区分不同控件
        // 2. 格式为"##标识符"：不显示标签，仅用"标识符"作为内部标识
        // 3. 无"##"：整个字符串既作为显示标签，也作为内部标识
        // 这里"##name"表示：不显示标签，内部用"name"作为标识
        ImGui::InputText("##name", name, IM_ARRAYSIZE(name));

        ImGui::Text("pass");  // 显示"pass"作为密码框的标签
        ImGui::SameLine();
        // 密码输入框：ImGuiInputTextFlags_Password标志使输入内容显示为*
        ImGui::InputText("##pass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);
        ImGui::InputText("p2ass", pass, IM_ARRAYSIZE(pass), ImGuiInputTextFlags_Password);

        // 带提示的输入框：当输入框为空时显示提示文本
        char hint_text[1024] = "mo ren ti shi";  // 提示文本
        ImGui::InputTextWithHint("##InputTextWithHint", hint_text,
            name, IM_ARRAYSIZE(name));

        // 多行输入框：允许输入多行文本
        ImGui::InputTextMultiline(
            "##MultiLineInput",  // 内部标识（不显示标签）
            input_text,          // 存储文本的缓冲区
            BUF_SIZE,            // 缓冲区最大容量
            ImVec2(0, 200)       // 输入框尺寸（宽度0表示自适应窗口，高度200像素）
        );

        // 加static让f变成静态变量，静态变量在函数中只会执行一次
        // 第一次执行当前函数会执行 static float f = 0.0f; 这一行代码，第二次执行当前函数时会跳过 static float f = 0.0f;这一行代码
        // 这样就能修改f的值后不会被重新赋值成0了
        static float f = 0.0f;
        // 滑块
        ImGui::SliderFloat("float", &f, 0.0f, 1.0f);
        ImGui::SliderFloat("##float", &f, 0.0f, 1.0f);

        // progress当前进度，progress_dir进度范围
        static float progress = 0.0f, progress_dir = 1.0f;
        progress += progress_dir * 0.4f * ImGui::GetIO().DeltaTime;
        // 第一个参数传当前进度，一个小数，第二个参数是进度条的长和高，第三个参数进度条里的描述
        ImGui::ProgressBar(progress, ImVec2(0.0f, 0.0f), "jinduxinxi");
        ImGui::ProgressBar(progress, ImVec2(300.0f, 20.0f));
        ImGui::SameLine(0.0f, ImGui::GetStyle().ItemInnerSpacing.x);
        ImGui::Text("Progress Bar");

        ImGui::End();  // 结束窗口定义（必须与ImGui::Begin配对使用）

        // 渲染UI：将定义的UI绘制到屏幕上
        ImGui::Render();  // 生成绘制命令列表

        // 计算背景色（考虑透明度）
        const float clear_color_with_alpha[4] = {
            clear_color.x * clear_color.w,
            clear_color.y * clear_color.w,
            clear_color.z * clear_color.w,
            clear_color.w
        };

        // 设置渲染目标：告诉GPU接下来的渲染输出到主渲染目标
        g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
        // 清空渲染目标：用背景色填充屏幕，清除上一帧的内容
        g_pd3dDeviceContext->ClearRenderTargetView(g_mainRenderTargetView,
            clear_color_with_alpha);
        // 渲染ImGui的UI：执行绘制命令
        ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

        // 显示画面：交换前后缓冲区，将渲染好的画面显示到屏幕上
        // Present()参数：
        // - 第一个参数：1表示开启垂直同步（VSync），0表示关闭
        // - 第二个参数：交换标志（0表示默认行为）
        HRESULT hr = g_pSwapChain->Present(1, 0);  // 开启垂直同步
        // 检查交换链是否被遮挡，用于下一次循环的优化
        g_SwapChainOccluded = (hr == DXGI_STATUS_OCCLUDED);
    }

    // 程序退出：清理所有资源
    // 关闭ImGui后端
    ImGui_ImplDX11_Shutdown();
    ImGui_ImplWin32_Shutdown();
    ImGui::DestroyContext();  // 销毁ImGui上下文

    // 清理D3D资源
    CleanupDeviceD3D();
    // 销毁窗口和窗口类
    ::DestroyWindow(hwnd);
    ::UnregisterClassW(wc.lpszClassName, wc.hInstance);

    return 0;  // 程序正常退出
}

```

## 12. 12.ImGui-外部绘制独立的界面窗体

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151578932
- Description: æç« æµè§éè¯»880æ¬¡ï¼ç¹èµ4æ¬¡ï¼æ¶è10æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imguiæ çªå£ç»å¶

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：11.ImGui-加载字体和中文 
到这ImGui基础的东西就搞完了，然后接下来绘制一个，正常的窗口，如下图现在绘制的东西都在下图红框里面，正常的窗口它应该是在下图黄框里面绘制控件（输入框、进度条、文本、单选框、复选框等） 
 
然后我们的程序运行后，它还有一个控制台，正常的窗口程序它也是没有控制台的，所以还要把控制台关了 
 
关闭控制台，鼠标右击选择属性 
 
如下图选择，把控制台改成窗口就可以关闭控制台了，选择完窗口然后点击确定 
 
再次运行会报错，因为控制台的入口函数和窗口的入口函数不一样 
 
把下图红框的main改成下图黄框的WinMain就可以了 
 
正常运行，然后控制台的问题就解决了，然后是窗口的问题 
 
然后再次来到ImGui的官网 
 
 https://github.com/ocornut/imgui 
 
然后点击下图蓝框的箭头，然后再点击下图红框 
 
然后再把它的docking版本的源码下载下来 
 
下载完后解压，不要放在中文的目录里，官网的代码没有中文字体 
 
它也有实例 
 
然后使用vs2022（vs几都可以，但最好跟我一样使用vs2022）打开它，如下图红框点击确定 
 
然后再找到directx11设置为启动项目 
 
效果图：可以看到它可以脱离下图黄框的窗口了，这样可以做的事情就多了 
 
修改它的代码后效果图：可以看到ImGui窗口的窗口脱离出来了 
 
这样运行后在任务栏，如下图会有三个 
 
上图左边第一个是通过，下图红框的代码创建的，如果想隐藏它可以使用CreateWindowExW 
 
如下图的代码 
 
效果图：这样搞完也会有其它的问题，窗口默认的关闭没了，需要自己写消息循环和ImGui的退出按钮 
 
然后还有一种方式，ImGui提供，如下图红框的代码， 
 
效果图：任务栏只有一个CreateWindowW创建的图标 
 
然后它实现脱离CreateWindowW窗口的代码，就比我们的代码多出了下图红框的代码，下一节将整合进去 
 
用到的代码和说明

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：11.ImGui-加载字体和中文 
到这ImGui基础的东西就搞完了，然后接下来绘制一个，正常的窗口，如下图现在绘制的东西都在下图红框里面，正常的窗口它应该是在下图黄框里面绘制控件（输入框、进度条、文本、单选框、复选框等） 
 
然后我们的程序运行后，它还有一个控制台，正常的窗口程序它也是没有控制台的，所以还要把控制台关了 
 
关闭控制台，鼠标右击选择属性 
 
如下图选择，把控制台改成窗口就可以关闭控制台了，选择完窗口然后点击确定 
 
再次运行会报错，因为控制台的入口函数和窗口的入口函数不一样 
 
把下图红框的main改成下图黄框的WinMain就可以了 
 
正常运行，然后控制台的问题就解决了，然后是窗口的问题 
 
然后再次来到ImGui的官网 
 
 https://github.com/ocornut/imgui 
 
然后点击下图蓝框的箭头，然后再点击下图红框 
 
然后再把它的docking版本的源码下载下来 
 
下载完后解压，不要放在中文的目录里，官网的代码没有中文字体 
 
它也有实例 
 
然后使用vs2022（vs几都可以，但最好跟我一样使用vs2022）打开它，如下图红框点击确定 
 
然后再找到directx11设置为启动项目 
 
效果图：可以看到它可以脱离下图黄框的窗口了，这样可以做的事情就多了 
 
修改它的代码后效果图：可以看到ImGui窗口的窗口脱离出来了 
 
这样运行后在任务栏，如下图会有三个 
 
上图左边第一个是通过，下图红框的代码创建的，如果想隐藏它可以使用CreateWindowExW 
 
如下图的代码 
 
效果图：这样搞完也会有其它的问题，窗口默认的关闭没了，需要自己写消息循环和ImGui的退出按钮 
 
然后还有一种方式，ImGui提供，如下图红框的代码， 
 
效果图：任务栏只有一个CreateWindowW创建的图标 
 
然后它实现脱离CreateWindowW窗口的代码，就比我们的代码多出了下图红框的代码，下一节将整合进去 
 
用到的代码和说明 

```text
// 定义窗口类扩展结构（WNDCLASSEXW 是 WNDCLASS 的扩展版本，支持额外成员）
// 用于描述窗口类的属性，注册后可基于该类创建窗口实例
WNDCLASSEXW wc = { 
    sizeof(wc),                  // cbSize：结构体自身大小（必须设置，用于系统验证）
    CS_CLASSDC,                  // style：窗口类样式，CS_CLASSDC 表示该类窗口共享一个设备上下文（DC）
    WndProc,                     // lpfnWndProc：窗口过程函数（回调），处理窗口消息（如点击、关闭等）
    0L, 0L,                      // cbClsExtra/cbWndExtra：类/窗口的额外数据字节数，此处无需额外数据
    GetModuleHandle(nullptr),    // hInstance：当前模块实例句柄（关联窗口所属的程序）
    nullptr,                     // hIcon：窗口类默认图标（nullptr 表示使用系统默认）
    nullptr,                     // hCursor：窗口类默认光标（nullptr 表示使用系统默认）
    nullptr,                     // hbrBackground：窗口背景画刷（nullptr 表示无默认背景，由程序自行绘制）
    nullptr,                     // lpszMenuName：默认菜单资源名（nullptr 表示无默认菜单）
    L"ImGui Example",            // lpszClassName：窗口类名（唯一标识，创建窗口时需匹配）
    nullptr                      // hIconSm：小图标（任务栏/标题栏小图标，nullptr 表示使用系统默认）
};

// 向系统注册窗口类
// 注册成功后，系统认可该窗口类，可基于此类创建窗口实例
::RegisterClassExW(&wc);

// 创建窗口实例（基于上面注册的窗口类）
HWND hwnd = ::CreateWindowW(
    wc.lpszClassName,            // lpClassName：窗口类名（必须与注册的类名一致）
    L"Dear ImGui DirectX11 Example", // lpWindowName：窗口标题（显示在标题栏，若有标题栏）
    WS_POPUP,                    // dwStyle：窗口样式，WS_POPUP 表示弹出窗口（无标题栏、边框等默认样式）
    100, 100,                    // x/y：窗口左上角在屏幕中的初始坐标（以像素为单位）
    1, 1,                        // nWidth/nHeight：窗口初始宽高（此处为 1x1 像素，通常会后续调整）
    nullptr,                     // hWndParent：父窗口句柄（nullptr 表示顶级窗口）
    nullptr,                     // hMenu：窗口菜单句柄（nullptr 表示无菜单）
    wc.hInstance,                // hInstance：当前模块实例句柄（与窗口类注册时一致）
    nullptr                      // lpParam：创建窗口时传递的额外数据（此处无需传递）
);
io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;         // 启用 Docking
io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;       // 启用多视口
// ConfigViewportsNoTaskBarIcon它的值是true时，禁止 ImGui 为独立视口创建任务栏图标。
// 使用时需要 有 ImGuiConfigFlags_DockingEnable 和 ImGuiConfigFlags_ViewportsEnable
io.ConfigViewportsNoTaskBarIcon = true;
```

## 13. 13.ImGui-搭建内部绘制的ImGui项目框架（无消息循环的简单ImGui实例）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151625711
- Description: æç« æµè§éè¯»1.1kæ¬¡ï¼ç¹èµ19æ¬¡ï¼æ¶è30æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_dll imgui

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：12.ImGui-外部绘制独立的界面窗体 
下面开始写代码了，代码看不懂没关系，要知道怎样去复制（写的很细全程傻瓜模式），代码的说明会放在最后（不放在最后，截图的时候不好截，看起来会很乱，用来说代码的来源会很不友好），说明用小白也能看懂的语言写的，看多了慢慢就知道了，不知道也没关系会复制会用就行 
到这ImGui的基础就可以了，然后接下来是如何在某程序内部使用ImGui绘制窗口 
首先打卡VisualStudio2022创建一个新项目 
 
内部绘制就要把我们程序放到目标程序里，也就是要用动态链接库，所以就创建一个动态链接库的项目，如下图红框 
 
随便输入一个项目名和保存位置，然后点击创建 
 
创建完成 
 
然后导入ImGui用到的库（文件） ，首先把下图红框的文件复制一下 
 
把复制的上图红框里的文件放到下图红框的目录，也就是上方创建项目的时候设置的那个目录 
 
然后创建一个文件夹 
 
然后再复制下图红框的两个文件 
 
把它们复制到刚刚创建的ImGui文件夹里，如下图红框 
 
然后在把下图红框的两个文件复制到ImGui文件夹中 
 
复制完后，文件相关的就完事了 
 
然后来到vs2022里，首先新加一个筛选器 
 
然后把下图红框里的4个文件拖到新加的筛选器里 
 
然后把下图红框的文件拖到源文件里 
 
然后右击头文件选择新建项 
 
创建一个main.h文件 
 
main.h里添加内容

```text
#pragma once
#include <d3d11.h>
#include "ImGui/imgui_impl_dx11.h"
#include "ImGui/imgui_impl_win32.h"

```
 
然后设置包含目录，如下图鼠标右击选择属性 
 
如下图设置包含目录 
 
添加 $(ProjectDir)，然后点击确定 
 
$(ProjectDir)是vs中内置的目录，它表示.vcxproj文件所在的目录，也就是下图红框文件的所在目录，这样写换个电脑就不用重新设置目录了，让vs自己找目录 
 
然后在给附加依赖项添加d3d11.lib; 如下图红框 
 
然后点击运行，会出现错误 
 
在预编译头里选择不使用预编译头，然后点击确定 
 
然后点击下图红框运行代码，会出现下图蓝框的提示，这是因为我们的项目是一个dll，不是exe这是正常的 
 
可以点击重新生成 
 
然后编译成功 
 
导致ImGui需要的东西就都搞完了，也都是之前的内容，然后接下来就开始写主要代码了，然后来到DllMain里，这是dll的入口，就是当dll放到目标程序里，就会执行DllMain里的代码

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：12.ImGui-外部绘制独立的界面窗体 
下面开始写代码了，代码看不懂没关系，要知道怎样去复制（写的很细全程傻瓜模式），代码的说明会放在最后（不放在最后，截图的时候不好截，看起来会很乱，用来说代码的来源会很不友好），说明用小白也能看懂的语言写的，看多了慢慢就知道了，不知道也没关系会复制会用就行 
到这ImGui的基础就可以了，然后接下来是如何在某程序内部使用ImGui绘制窗口 
首先打卡VisualStudio2022创建一个新项目 
 
内部绘制就要把我们程序放到目标程序里，也就是要用动态链接库，所以就创建一个动态链接库的项目，如下图红框 
 
随便输入一个项目名和保存位置，然后点击创建 
 
创建完成 
 
然后导入ImGui用到的库（文件） ，首先把下图红框的文件复制一下 
 
把复制的上图红框里的文件放到下图红框的目录，也就是上方创建项目的时候设置的那个目录 
 
然后创建一个文件夹 
 
然后再复制下图红框的两个文件 
 
把它们复制到刚刚创建的ImGui文件夹里，如下图红框 
 
然后在把下图红框的两个文件复制到ImGui文件夹中 
 
复制完后，文件相关的就完事了 
 
然后来到vs2022里，首先新加一个筛选器 
 
然后把下图红框里的4个文件拖到新加的筛选器里 
 
然后把下图红框的文件拖到源文件里 
 
然后右击头文件选择新建项 
 
创建一个main.h文件 
 
main.h里添加内容 
 

```text
#pragma once
#include <d3d11.h>
#include "ImGui/imgui_impl_dx11.h"
#include "ImGui/imgui_impl_win32.h"

```
 
然后设置包含目录，如下图鼠标右击选择属性 
 
如下图设置包含目录 
 
添加 $(ProjectDir)，然后点击确定 
 
$(ProjectDir)是vs中内置的目录，它表示.vcxproj文件所在的目录，也就是下图红框文件的所在目录，这样写换个电脑就不用重新设置目录了，让vs自己找目录 
 
然后在给附加依赖项添加d3d11.lib; 如下图红框 
 
然后点击运行，会出现错误 
 
在预编译头里选择不使用预编译头，然后点击确定 
 
然后点击下图红框运行代码，会出现下图蓝框的提示，这是因为我们的项目是一个dll，不是exe这是正常的 
 
可以点击重新生成 
 
然后编译成功 
 
导致ImGui需要的东西就都搞完了，也都是之前的内容，然后接下来就开始写主要代码了，然后来到DllMain里，这是dll的入口，就是当dll放到目标程序里，就会执行DllMain里的代码 
 

```text
// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "pch.h"
/**
 * DllMain：Windows动态链接库(DLL)的入口点函数
 * 当DLL被加载到进程、线程创建/销毁、DLL被卸载时，系统会自动调用该函数
 * 用于执行DLL的初始化、资源分配、清理等操作
 *
 * 参数说明：
 * - hModule：DLL的模块句柄（HMODULE），可理解为DLL在内存中的唯一标识
 *            类似于EXE的实例句柄，可用于加载资源、获取路径等
 * - ul_reason_for_call：调用该函数的原因（触发事件），为DWORD类型
 * - lpReserved：保留参数，用于传递额外信息，不同事件含义不同
 *
 * 返回值：BOOL类型
 * - 对于DLL_PROCESS_ATTACH事件：返回TRUE表示DLL加载成功；返回FALSE会导致加载失败
 * - 其他事件：返回值通常被忽略（系统不处理）
 */
BOOL APIENTRY DllMain(
    HMODULE hModule,        // DLL模块句柄（当前DLL的标识）
    DWORD  ul_reason_for_call,  // 调用原因（触发的事件类型）
    LPVOID lpReserved       // 保留参数（不同事件含义不同）
)
{
    // 根据调用原因处理不同事件
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // 事件含义：DLL被成功加载到某个进程的地址空间时触发
        // 触发时机：进程首次加载DLL时（如通过LoadLibrary函数）
        // 典型用途：初始化DLL的全局资源（如分配内存、创建对象、注册回调）
        // 注意：此时进程的主线程可能还未开始执行，避免在此创建UI或复杂操作
        // lpReserved：若为NULL，表示DLL是被显式加载（如LoadLibrary）；非NULL表示隐式加载（如依赖项加载）
        break;

    case DLL_THREAD_ATTACH:
        // 事件含义：进程中创建新线程时，系统会通知所有已加载的DLL
        // 触发时机：新线程启动时（线程函数执行前）
        // 典型用途：为新线程分配专属资源（如线程局部存储TLS）
        // 注意：每个新线程创建都会触发，需避免资源泄露
        // lpReserved：始终为NULL
        break;

    case DLL_THREAD_DETACH:
        // 事件含义：进程中的线程结束时，系统会通知所有已加载的DLL
        // 触发时机：线程正常退出时（线程函数返回后）
        // 典型用途：释放该线程在DLL中分配的专属资源（如TLS中的数据）
        // 注意：若线程异常终止（如TerminateThread），此事件不会触发
        // lpReserved：始终为NULL
        break;

    case DLL_PROCESS_DETACH:
        // 事件含义：DLL从进程的地址空间中卸载时触发
        // 触发时机：进程调用FreeLibrary释放DLL，或进程退出时
        // 典型用途：释放DLL_PROCESS_ATTACH中分配的全局资源（如内存、文件句柄）
        // 注意：若进程退出（如ExitProcess），部分系统资源可能已失效，避免复杂操作
        // lpReserved：若为NULL，表示DLL被显式卸载（如FreeLibrary）；非NULL表示进程正在退出
        break;
    }

    // 返回TRUE表示所有事件处理成功
    // 对于DLL_PROCESS_ATTACH，返回FALSE会导致DLL加载失败
    return TRUE;
}

```
 
然后创建一个MyDx.h和MyDx.cpp文件 
 
然后在main.h文件中添加下图红框的内容 #include <windows.h> 
 
MyDx.h的内容 
 

```text
#pragma once
// 声明一个函数叫做Go
DWORD Go(
    LPVOID lpThreadParameter
);

```
 
MyDx.pp的内容 
 

```text
#include "main.h"
// 实现Go函数
DWORD Go(
    LPVOID lpThreadParameter
) {

    return 0;
}

```
 
然后dllmain.cpp里的内容 
 

```text
// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "main.h"
/**
 * DllMain：Windows动态链接库(DLL)的入口点函数
 * 当DLL被加载到进程、线程创建/销毁、DLL被卸载时，系统会自动调用该函数
 * 用于执行DLL的初始化、资源分配、清理等操作
 *
 * 参数说明：
 * - hModule：DLL的模块句柄（HMODULE），可理解为DLL在内存中的唯一标识
 *            类似于EXE的实例句柄，可用于加载资源、获取路径等
 * - ul_reason_for_call：调用该函数的原因（触发事件），为DWORD类型
 * - lpReserved：保留参数，用于传递额外信息，不同事件含义不同
 *
 * 返回值：BOOL类型
 * - 对于DLL_PROCESS_ATTACH事件：返回TRUE表示DLL加载成功；返回FALSE会导致加载失败
 * - 其他事件：返回值通常被忽略（系统不处理）
 */
BOOL APIENTRY DllMain(
    HMODULE hModule,        // DLL模块句柄（当前DLL的标识）
    DWORD  ul_reason_for_call,  // 调用原因（触发的事件类型）
    LPVOID lpReserved       // 保留参数（不同事件含义不同）
)
{
    // 根据调用原因处理不同事件
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
        // 事件含义：DLL被成功加载到某个进程的地址空间时触发
        // 触发时机：进程首次加载DLL时（如通过LoadLibrary函数）
        // 典型用途：初始化DLL的全局资源（如分配内存、创建对象、注册回调）
        // 注意：此时进程的主线程可能还未开始执行，避免在此创建UI或复杂操作
        // lpReserved：若为NULL，表示DLL是被显式加载（如LoadLibrary）；非NULL表示隐式加载（如依赖项加载）
        // 启动一个线程调用Go函数
        ::CreateThread(0,0,Go,0,0,0);
        break;

    case DLL_THREAD_ATTACH:
        // 事件含义：进程中创建新线程时，系统会通知所有已加载的DLL
        // 触发时机：新线程启动时（线程函数执行前）
        // 典型用途：为新线程分配专属资源（如线程局部存储TLS）
        // 注意：每个新线程创建都会触发，需避免资源泄露
        // lpReserved：始终为NULL
        break;

    case DLL_THREAD_DETACH:
        // 事件含义：进程中的线程结束时，系统会通知所有已加载的DLL
        // 触发时机：线程正常退出时（线程函数返回后）
        // 典型用途：释放该线程在DLL中分配的专属资源（如TLS中的数据）
        // 注意：若线程异常终止（如TerminateThread），此事件不会触发
        // lpReserved：始终为NULL
        break;

    case DLL_PROCESS_DETACH:
        // 事件含义：DLL从进程的地址空间中卸载时触发
        // 触发时机：进程调用FreeLibrary释放DLL，或进程退出时
        // 典型用途：释放DLL_PROCESS_ATTACH中分配的全局资源（如内存、文件句柄）
        // 注意：若进程退出（如ExitProcess），部分系统资源可能已失效，避免复杂操作
        // lpReserved：若为NULL，表示DLL被显式卸载（如FreeLibrary）；非NULL表示进程正在退出
        break;
    }

    // 返回TRUE表示所有事件处理成功
    // 对于DLL_PROCESS_ATTACH，返回FALSE会导致DLL加载失败
    return TRUE;
}

```
 
 
然后上方的Go函数实现还没完，我们的ImGui的代码要写在Go函数里，所以接下来开始复制ImGui的代码，下图蓝框的代码是创建一个窗口，现在我们是内部窗口目标程序已经有窗口了，所以现在不需要它们，直接从CreateDeviceD3D开始 
 
把下图红框的代码全部复制， 
 
复制过来后补齐代码，都是从ImGui源码里复制的 
 
复制方式，来到ImGui源码里，然后找到缺少的代码，按着CTRL然后鼠标左键单击，就会给跳到它的声明位置（声明可以理解为创建） 
 
就会跳到下图红框位置，把它复制过去就可以了 
 
然后再补全CreateRenderTarget函数，按着CTRL鼠标左键单击下图红框位置 
 
跳到CreateRenderTarget函数后，把下图红框的代码复制过去 
 
复制过来后，可以看到它缺少 g_mainRenderTargetView，再找g_mainRenderTargetView 
 
按着CTRL使用鼠标左键单击下图红框位置 
 
然后它就跳转到下图红框位置，把下图红框代码复制过去 
 
然后就不报错了 
 
下方就不贴复制后的图了，只贴需要复制的代码的图，默认把它们依次复制过去就行 
然后是创建ImGui的上下文，也就是让ImGui初始化它需要的数据（上下文可以理解为需要的数据） 
 
然后是ImGui的样式 
 
然后是初始化WIn32（连接ImGui与Windows窗口系统）和DirectX 11（连接ImGui与DirectX 11渲染系统） 
 
然后是Begin和End 
 
然后数渲染视图 
 
然后绑定视图 
 
连接DirectX 11 
 
复制完的代码 
 
重新生成，可以正常生成 
 
以上就是一个从官方的实例中摘出来的最简单最基本的ImGui实例，想要运行还需要把渲染的代码放到虚表里，下一节hook虚表，然后把我们的代码放进去 
带说明的代码，由Ai生成 

```text
// 包含程序所需的头文件（通常包含DirectX、ImGui等库的声明）
#include "main.h"

// 获取目标窗口的句柄（HWND）
// FindWindowA参数说明：
// - 第一个参数：窗口类名（为空字符串表示不限制类名）
// - 第二个参数：窗口标题（NULL表示查找任何窗口）
// 作用：获取一个已存在窗口的句柄，后续DirectX渲染会输出到该窗口
HWND hWnd = FindWindowA("", NULL);

// DirectX 11核心全局资源（整个程序共享）
static ID3D11Device* g_pd3dDevice = nullptr;               // D3D11设备对象，负责创建渲染资源
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // D3D11设备上下文，负责执行渲染命令
static IDXGISwapChain* g_pSwapChain = nullptr;             // 交换链对象，管理前后缓冲区实现双缓冲
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 主渲染目标视图，绑定交换链的后台缓冲区

/**
 * 线程函数：负责初始化DirectX 11和ImGui，并执行首次UI渲染
 * 函数签名符合Windows线程函数要求（LPVOID参数，返回DWORD）
 * 参数：
 * - lpThreadParameter：线程启动时传递的参数（此处未使用）
 * 返回值：DWORD类型，0通常表示执行成功
 */
DWORD Go(
    LPVOID lpThreadParameter  // 线程参数（未使用，保留为兼容线程函数签名）
) {
    // 初始化交换链描述结构体（DXGI_SWAP_CHAIN_DESC），定义交换链的属性
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd));  // 清空结构体，避免未初始化内存导致的错误

    // 配置交换链核心参数
    sd.BufferCount = 2;                   // 缓冲区数量（双缓冲：1个前台显示，1个后台渲染）
    sd.BufferDesc.Width = 0;              // 缓冲区宽度（0表示自动匹配窗口宽度）
    sd.BufferDesc.Height = 0;             // 缓冲区高度（0表示自动匹配窗口高度）
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM;  // 像素格式（32位RGBA，8位/通道）
    sd.BufferDesc.RefreshRate.Numerator = 60;  // 刷新率分子（60Hz）
    sd.BufferDesc.RefreshRate.Denominator = 1; // 刷新率分母（60/1=60Hz）
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH;  // 允许切换显示模式（窗口/全屏）
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;   // 缓冲区用途（作为渲染目标）
    sd.OutputWindow = hWnd;               // 绑定的窗口句柄（渲染结果输出到该窗口）
    sd.SampleDesc.Count = 1;              // 多重采样数量（1表示无抗锯齿）
    sd.SampleDesc.Quality = 0;            // 采样质量（0表示默认）
    sd.Windowed = TRUE;                   // 窗口模式（TRUE为窗口化，FALSE为全屏）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD;  // 交换效果（交换后丢弃后台缓冲区数据）

    // 创建设备的标志（可添加调试标志）
    UINT createDeviceFlags = 0;
    // createDeviceFlags |= D3D11_CREATE_DEVICE_DEBUG;  // 启用调试模式（需要安装DirectX SDK）

    D3D_FEATURE_LEVEL featureLevel;  // 存储实际支持的Direct3D特性级别（版本）
    // 支持的D3D版本列表（优先使用11.0，不支持则降级到10.0）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { 
        D3D_FEATURE_LEVEL_11_0, 
        D3D_FEATURE_LEVEL_10_0 
    };

    // 创建设备、设备上下文和交换链
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr,                       // 显卡适配器（nullptr使用默认显卡）
        D3D_DRIVER_TYPE_HARDWARE,      // 驱动类型（硬件加速，使用GPU）
        nullptr,                       // 软件渲染模块（未使用）
        createDeviceFlags,             // 创建设备的标志
        featureLevelArray,             // 支持的D3D版本列表
        2,                             // 版本列表数量
        D3D11_SDK_VERSION,             // SDK版本（使用当前版本）
        &sd,                           // 交换链描述结构体
        &g_pSwapChain,                 // 输出：创建的交换链
        &g_pd3dDevice,                 // 输出：创建的D3D设备
        &featureLevel,                 // 输出：实际支持的D3D版本
        &g_pd3dDeviceContext           // 输出：创建的设备上下文
    );

    // 若硬件加速失败（如显卡不支持D3D11），尝试使用WARP软件渲染驱动
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP,  // 软件渲染驱动（CPU模拟GPU）
            nullptr, createDeviceFlags,
            featureLevelArray, 2,
            D3D11_SDK_VERSION, &sd,
            &g_pSwapChain, &g_pd3dDevice,
            &featureLevel, &g_pd3dDeviceContext
        );

    // 若设备/交换链创建失败，返回错误（0表示成功，此处返回false可能是笔误，应为非0）
    if (res != S_OK)
        return false;

    // 获取交换链的后台缓冲区（用于创建渲染目标视图）
    ID3D11Texture2D* pBackBuffer;  // 临时指针，存储后台缓冲区
    g_pSwapChain->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer));  // 0表示第一个缓冲区

    // 使用后台缓冲区创建渲染目标视图（告诉GPU渲染结果输出到这里）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release();  // 释放临时缓冲区指针（渲染目标视图已引用该资源）

    // 初始化ImGui上下文（管理UI状态和资源的核心对象）
    ImGui::CreateContext();
    // 设置ImGui的UI风格为暗色主题（内置风格之一，还有亮色、经典风格等）
    ImGui::StyleColorsDark();

    // 初始化ImGui的Win32后端（连接ImGui与Windows窗口系统，处理输入事件）
    ImGui_ImplWin32_Init(hWnd);
    // 初始化ImGui的DX11后端（连接ImGui与DirectX 11，负责UI渲染）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext);

    // 定义一个ImGui窗口（"Hello, world!"为窗口标题）
    // 注意：正常流程中，窗口定义应放在NewFrame()之后、Render()之前的主循环内
    // 此处直接调用Begin/End缺少帧初始化，可能导致UI无法正确显示
    ImGui::Begin("Hello, world!");  // 开始定义窗口内容（此处无实际内容）
    ImGui::End();  // 结束窗口定义

    // 生成UI绘制数据（将窗口/控件转换为GPU可识别的绘制命令）
    ImGui::Render();

    // 设置渲染目标（告诉GPU接下来的渲染输出到主渲染目标）
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    // 通过DX11后端执行绘制命令，将ImGui UI渲染到屏幕上
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    // 线程执行完成，返回0表示成功
    return 0;
}
    

```
 
AI生成的总结 
 
 上方代码的核心目的：在一个已有的 Windows 窗口上，用 DirectX11（负责画图的工具）和 ImGui（快速做 UI 的库），画一个简单的 “Hello, world!” 窗口。 
 一、先搞懂 3 个关键工具是干嘛的 
 在看代码前，先记 3 个 “小角色”： 
 DirectX11：相当于 “画笔 + 画布”，负责把图像（比如按钮、文本）画到屏幕上；ImGui：相当于 “UI 模板库”，不用自己写按钮、窗口的底层代码，直接调用现成的功能；Windows 窗口句柄（hWnd）：相当于 “贴画的地方”，UI 最终要画在这个窗口上。 
 二、代码分 5 步走：从 “准备工具” 到 “画出 UI” 
 第 1 步：找到要画 UI 的窗口（找 “贴画的地方”） 
 
```text
HWND hWnd = FindWindowA("", NULL);

```
 
 作用：找一个已经存在的 Windows 窗口（比如记事本、浏览器窗口），hWnd就是这个窗口的 “身份证号”；小白注意：这里参数是空的，可能会找到 “不对的窗口”（比如本来想画在游戏窗口，结果画在了桌面窗口），实际用的时候要填窗口标题或类名。 
 第 2 步：初始化 DirectX11（准备 “画笔 + 画布”） 
 这部分是最复杂的，但核心就干 3 件事： 
 创建 “设备（g_pd3dDevice）”：相当于 “画笔工厂”，负责造画图需要的各种工具（比如画 UI 的颜色、形状）；创建 “交换链（g_pSwapChain）”：相当于 “双画布”，一个画布显示当前画面，另一个画布偷偷画下一针，画完再切换，避免画面闪烁；创建 “渲染目标（g_mainRenderTargetView）”：相当于 “指定画布的作画区域”，告诉 DirectX “UI 要画在交换链的这个区域里”。 
 小白注意：如果显卡不支持 DirectX11，代码会自动用 “软件渲染”（用 CPU 模拟显卡，速度慢但能跑）。 
 第 3 步：初始化 ImGui（准备 “UI 模板”） 
 
```text
ImGui::CreateContext();       // 开一个ImGui的“工作环境”
ImGui::StyleColorsDark();     // 给UI选个风格（这里是深色主题，还有亮色、经典款）
ImGui_ImplWin32_Init(hWnd);   // 让ImGui能“认”这个Windows窗口，处理鼠标/键盘输入
ImGui_ImplDX11_Init(...)      // 让ImGui能“用”DirectX11的画笔，把UI画出来

```
 
 作用：把 ImGui 和 Windows 窗口、DirectX11 连起来，不然 ImGui 不知道该画在哪、用什么工具画。 
 第 4 步：定义要画的 UI（选 “UI 模板”） 
 
```text
ImGui::Begin("Hello, world!");  // 新建一个窗口，标题是“Hello, world!”
ImGui::End();                   // 窗口定义结束（这里窗口里没内容，只有个空标题栏）

```
 
 小白注意：这就像搭积木，Begin是 “开始搭一个窗口”，中间可以加按钮（ImGui::Button）、文本（ImGui::Text），End是 “搭完这个窗口”。 
 第 5 步：把 UI 画到屏幕上（动手 “贴画”） 
 
```text
ImGui::Render();                       // 让ImGui把定义好的UI转换成“画图指令”
g_pd3dDeviceContext->OMSetRenderTargets(...);  // 告诉DirectX“接下来画到这个区域”
ImGui_ImplDX11_RenderDrawData(...);    // 让DirectX执行画图指令，把UI画出来

```
 
 作用：从 “纸上谈兵”（定义 UI）到 “实际动手”（画到屏幕），这一步才是真正让 UI 显示出来。 
 三、小白要注意的 3 个 “坑” 
 没有 “循环”，UI 只显示一次：这段代码画完一次 UI 就结束了，没法互动（比如点按钮没反应）。实际用的时候要加个while循环，让代码反复画 UI、处理输入；没 “清理垃圾”：代码创建的 DirectX 和 ImGui 资源（比如设备、交换链）没释放，程序关了可能还占内存。要在最后加Release()（释放 DirectX 资源）和Shutdown()（关闭 ImGui）；找窗口可能找错：FindWindowA("", NULL)会找 “任意窗口”，如果开了多个程序，可能画错地方。要改成FindWindowA("窗口类名", "窗口标题")（比如找记事本窗口，标题是 “无标题 - 记事本”）。 
 四、整体逻辑一句话总结 
 找一个窗口 → 准备好画图工具（DirectX11） → 准备好 UI 模板（ImGui） → 选一个 UI 模板（空窗口） → 用工具把 UI 画到窗口上。

## 14. 14.ImGui-DX11虚表hook（一）-认识虚表（全局虚表说明）

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151656740
- Description: æç« æµè§éè¯»1.6kæ¬¡ï¼ç¹èµ54æ¬¡ï¼æ¶è15æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ èè¡¨ C++èè¡¨_dx11äº¤æ¢é¾å½æ°

### Summary

(No content extracted)

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：13.ImGui-搭建内部绘制的ImGui项目框架（无消息循环的简单ImGui实例） 
虚表hook是通过dx11的交换链得到虚表，然后进行hook，交换链就是下图红框的东西 
 
然后下图红框它的类型，然后按着CTRL然后鼠标左键单击下图红框位置 
 
然后就能来到下图红框位置，这是一个c++类（类可以理解为一个结构），结构的名字是 IDXGISwapChain，这个结构用来描述DX11的交换链数据 
 
如下图红框有很多函数它前面都有virtual，函数中有这个virtual都被称为虚函数，虚表就是用来存放虚函数的，然后代码编译成程序后（dll或exe）虚表的位置就会放在结构中第一个位置上，虚表的地址是同对象共享的（如果不理解，看下方的代码示例图），然后要hook的是Present函数，它是DX11用来渲染的函数 
 
然后虚表很重要，所以下面开始介绍虚表，首先打开vs2022，创建一个控制台项目，如下图点击创建新项目 
 
选择控制台应用，然后点击下一步 
 
然后设置项目名和存放位置，然后点击创建 
 
创建完后 
 
然后写两个类，如下图红框，一个叫Object类，一个叫BOOS类，BOOS类继承Object类，上方的DX11交换链的结构是IDXGISwapChain类继承IDXGIDeviceSubObject类，跟下图的同理 
 
然后使用上方的boos类 
 
然后点击下图红框位置设置断点 
 
设置了断点后的样子，有个小红点就表示设置了断点，当程序运行到设置了断点的位置后，会停下来 
 
然后如下图红框当前是64位Debug模式 
 
然后点击下图红框运行 
 
运行后在断点位置停下来了 
 
然后把内存窗口打开 
 
内存窗口打开之后 
 
然后下图红框的单词加&就可以得到boos的首地址了，然后boos是BOOS类型，也就是得到了BOOS类的首地址，&boos 
 
然后在下图红框输入&boos，然后按回车键（Enter键） 
 
然后就跳转到了boos的首地址，下图红框就是boos在内存中的样子了，现在还么有初始化所以全是CC 
 
然后点击下图红框停止一下 
 
然后改一下代码，如下图红框，改代码的愿意是为了在内存中让我们好区分，可以看到下图红框的数字前面有0x，这个表示当前数字是十六进制的，然后内存中的数据都会使用十六进制，如果不加0x就会是十进制，到了内存里我需要换算，不够直观，所以直接加上0x让它变成十六进制数方便在内存中观察 
 
然后再次运行后，输入&boos来到它的首地址，如下图红框 
 
然后点击下图红框，让它运行一行代码 
 
按了上图红框的按钮后就会执行，下图红框的代码，然后boos就会被初始化，初始化后就有数据了，数据如下图绿框 
 
如下图红框可以看到200和5000，0050是5000，0002是0200也就是200，要反着看，然后可以发现它先是Object类型的数据，也就是父类的数据，然后再是BOOS的数据 
 
然后最前面的，如下图红框就是虚表（虚表的地址） 
 
然后使用内存窗口访问虚表地址0x00007ff6c981ac50，它是十六进制数要带着0x，然后下图红框输入0x00007ff6c981ac50，然后按回车键 
 
然后如下图红框就来到了虚表，然后可以看到全是数字不认识，不会看 
 
然后鼠标左键右击选择转到反汇编 
 
然后就能看到函数的地址了，如下图的框框，然后拿着这些地址去内存窗口里的虚表中找，就能认识了 
 
如下图的框框 
 
虚函数在虚表中的位置，如下图，可以发现它是以编写的顺序而定的 
 
然后也就是说，一个类如果有虚函数，那么在它的首地址到首地址+8字节的位置是虚表地址，就是可以看到内存里是两个数一组两个数一组，两个数就是1个字节，如下图的8个框就是8字节，一个框表示1字节，两个数字表示1字节，00开头会默认省略不显示（可以在上方的实例中看到它省略了开头的0），64位是8字节，32位是4字节，这里用的是64位，32位和64位一样所以不展示32了 
 
然后虚表结束后就是类中的数据，下图红框的就是数据，它们的数据是int类型，int类型是4字节，这种数据被称为成员变量 
 
然后如果有继承关系，父（Object）类的数据会在前面，子（BOOS）类的数据会在后面 
 
虚函数也是如此，父（Object）类的虚函数在前面，子（BOOS）类的虚函数在后面 
 
然后是虚表是全局的，这就导致了同类型的虚表都是共享同一个，如下图，可以看到X类型有tmp1和tmp2，它们的虚表地址是一样的，然后Z类型有z1和z2它们的虚表地址也是一样的，通过下图是可以很清晰的认出 同一类对象共享全局虚表，这个是C++语言的特性，C++ 虚表的全局共享性，是多态底层的实现方式

## 15. 15.ImGui-DX11虚表hook（二）-实现hook虚表dx11

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151762943
- Description: æç« æµè§éè¯»2kæ¬¡ï¼ç¹èµ60æ¬¡ï¼æ¶è10æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ DirectX11_dx11 hook

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：14.ImGui-DX11虚表hook（一）-认识虚表 
现在要hook下图红框函数，就要找到它的内存地址 
 
类的地址可以通过下图红框的交换链变量得到 
 
然后就要找Present函数在虚表中的位置，要指定它在虚表中的位置就要先看父类，然后按着CTRL鼠标左键单击下图红框位置进入父类 
 
进入父类中可以看到有1个虚函数，然后它还有个叫IDXGIObject的父类 
 
然后再按着CTRL鼠标左键单击父类，进入IDXGIObject类中，如下图红框，可以看到它有4个虚函数，然后它还有个叫IUnknown的父类 
 
然后再按着CTRL鼠标左键单击父类，进入IUnknown类中，如下图红框它有3个虚函数，然后没有父类了 
 
然后首先通过g_pSwapChain得到IDXGISwapChain类的内存地址，得到虚表的内存地址，然后通过虚表的内存地址进入虚表，然后读第8个位置+1位置就是Present函数地址了，然后开始写代码，首先写下图红框的代码，引入iostream库，后面要用控制台打印（printf函数），不引入iostream会报错 
 
然后下图红框是我们自己声明的Present函数，函数的说明会放到最后会很详细，这里只要知道是我们自己声明的Present函数就可以了 
 
然后再写下图红框的代码 
 
然后手动打开控制台 
 
然后重新编译会出错，这是因为使用了不安全的函数，需要进行设置一下，首先复制下图红框 
 
然后鼠标右击选择属性 
 
然后点击下图红框的编辑 
 
然后把复制的内容放在第一行，然后点击确定 
 
然后重新编译就可以成功了 
 
然后填上窗口类名（类名是根据窗口来的，游戏会有保护spy++没办法获取，后面会写怎么办） 
 
然后把下图红框的代码全部注释，然后再重新编译，如果不注释会因为ImGui导致游戏崩溃 
 
然后随便找一个使用dx11渲染的游戏，这个代码只要是dx11渲染的都可以使用，进行注入测试，下图打开注入器，然后点击选择，然后点击窗口列表，然后找到要注入的程序，找到后双击选择 
 
如下图选择要注入的程序后 
 
然后点击下图红框的添加 
 
然后鼠标右击文件，选择打开所在的文件夹 
 
然后来到下图红框的目录，vs2022重新生成后才会有 
 
然后再来到注入器，选择我们的dll文件，然后点击打开 
 
打开之后，然后点击注入就可以把我们的dll文件放到游戏中了 
 
如下图测试成功 
 
完整代码

```text
// 包含必要头文件（DirectX、Windows API等核心功能定义）
#include "main.h"

// 1. 获取Unreal引擎游戏窗口句柄（目标窗口）
// 参数1："UnrealWindow"是Unreal引擎游戏的标准窗口类名（所有同引擎游戏通用）
// 参数2：NULL表示匹配任何标题的该类窗口
// 作用：定位到要Hook的游戏窗口，后续渲染和Hook操作都针对此窗口
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量）
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建渲染资源（如纹理、缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（如画图、切换缓冲区）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 交换链：管理前后缓冲区（核心对象，用于找到虚表）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：指定画面输出区域

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：14.ImGui-DX11虚表hook（一）-认识虚表 
现在要hook下图红框函数，就要找到它的内存地址 
 
类的地址可以通过下图红框的交换链变量得到 
 
然后就要找Present函数在虚表中的位置，要指定它在虚表中的位置就要先看父类，然后按着CTRL鼠标左键单击下图红框位置进入父类 
 
进入父类中可以看到有1个虚函数，然后它还有个叫IDXGIObject的父类 
 
然后再按着CTRL鼠标左键单击父类，进入IDXGIObject类中，如下图红框，可以看到它有4个虚函数，然后它还有个叫IUnknown的父类 
 
然后再按着CTRL鼠标左键单击父类，进入IUnknown类中，如下图红框它有3个虚函数，然后没有父类了 
 
然后首先通过g_pSwapChain得到IDXGISwapChain类的内存地址，得到虚表的内存地址，然后通过虚表的内存地址进入虚表，然后读第8个位置+1位置就是Present函数地址了，然后开始写代码，首先写下图红框的代码，引入iostream库，后面要用控制台打印（printf函数），不引入iostream会报错 
 
然后下图红框是我们自己声明的Present函数，函数的说明会放到最后会很详细，这里只要知道是我们自己声明的Present函数就可以了 
 
然后再写下图红框的代码 
 
然后手动打开控制台 
 
然后重新编译会出错，这是因为使用了不安全的函数，需要进行设置一下，首先复制下图红框 
 
然后鼠标右击选择属性 
 
然后点击下图红框的编辑 
 
然后把复制的内容放在第一行，然后点击确定 
 
然后重新编译就可以成功了 
 
然后填上窗口类名（类名是根据窗口来的，游戏会有保护spy++没办法获取，后面会写怎么办） 
 
然后把下图红框的代码全部注释，然后再重新编译，如果不注释会因为ImGui导致游戏崩溃 
 
然后随便找一个使用dx11渲染的游戏，这个代码只要是dx11渲染的都可以使用，进行注入测试，下图打开注入器，然后点击选择，然后点击窗口列表，然后找到要注入的程序，找到后双击选择 
 
如下图选择要注入的程序后 
 
然后点击下图红框的添加 
 
然后鼠标右击文件，选择打开所在的文件夹 
 
然后来到下图红框的目录，vs2022重新生成后才会有 
 
然后再来到注入器，选择我们的dll文件，然后点击打开 
 
打开之后，然后点击注入就可以把我们的dll文件放到游戏中了 
 
如下图测试成功 
 
完整代码 

```text
// 包含必要头文件（DirectX、Windows API等核心功能定义）
#include "main.h"

// 1. 获取Unreal引擎游戏窗口句柄（目标窗口）
// 参数1："UnrealWindow"是Unreal引擎游戏的标准窗口类名（所有同引擎游戏通用）
// 参数2：NULL表示匹配任何标题的该类窗口
// 作用：定位到要Hook的游戏窗口，后续渲染和Hook操作都针对此窗口
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量）
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建渲染资源（如纹理、缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（如画图、切换缓冲区）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 交换链：管理前后缓冲区（核心对象，用于找到虚表）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：指定画面输出区域

// 3. 定义Present函数类型（遵循IDXGISwapChain接口标准）
// Present函数是交换链用于"显示画面"的核心函数（将后台绘制好的画面展示到屏幕）
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,  // 调用该函数的交换链对象（谁调用就是谁的指针）
    UINT SyncInterval,     // 垂直同步参数（0=关闭，1=开启）
    UINT Flags             // 显示控制标志（通常为0）
);
Present MyPresent; // 存储游戏原始的Present函数地址（用于Hook后继续调用）

// 4. 自定义的Hook函数（替换游戏的Present函数）
// 当游戏调用Present显示画面时，会先执行此函数
HRESULT VtPresent(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
) {
    // 这里可以添加自定义操作（如绘制UI、修改画面等）
    printf("游戏正在显示画面，已被Hook！\n");

    // 调用游戏原始的Present函数（必须调用，否则游戏画面无法显示）
    return MyPresent(This, SyncInterval, Flags);
}

// 5. 线程函数：创建组件并完成Hook（核心逻辑）
DWORD Go(LPVOID lpThreadParameter) {
    // 5.1 配置交换链参数（创建符合标准的交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd)); // 清空参数结构体，避免随机值错误
    sd.BufferCount = 2;          // 双缓冲区（1个显示，1个后台绘制）
    sd.BufferDesc.Width = 0;     // 宽度自动匹配窗口
    sd.BufferDesc.Height = 0;    // 高度自动匹配窗口
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM; // 32位RGBA颜色格式
    sd.BufferDesc.RefreshRate.Numerator = 60; // 刷新率60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH; // 允许窗口/全屏切换
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 缓冲区用于显示画面
    sd.OutputWindow = hWnd;      // 绑定到游戏窗口
    sd.SampleDesc.Count = 1;     // 无抗锯齿
    sd.Windowed = TRUE;          // 窗口模式
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD; // 交换后丢弃后台数据（性能最优）

    // 5.2 创建设备和交换链（关键步骤：创建标准的IDXGISwapChain实例）
    UINT createDeviceFlags = 0;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );
    // 若硬件加速失败，尝试软件渲染（兼容性处理）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );
    if (res != S_OK) return false; // 创建失败则退出

    // 6. 核心Hook逻辑（利用C++虚表共享特性）
    // 6.1 获取IDXGISwapChain接口的"全局共享虚表"
    // 关键原理1：虚表（VirtualTable）属于"接口类型"（IDXGISwapChain），而非"对象实例"
    // 所有通过该接口创建的对象（包括游戏的交换链和我们的g_pSwapChain），都共用这一份虚表
    // 类比：所有iPhone 15共用同一份官方说明书，而非每台手机单独一份
    DWORD64* VirtualTable = *(DWORD64**)g_pSwapChain; 
    // 解析：g_pSwapChain是接口实例，其第一个成员是"虚表指针"，指向全局共享虚表

    // 6.2 保存原始Present函数地址（虚表第8个位置，微软标准规定）
    // 关键原理2：微软定义IDXGISwapChain接口时，将Present函数固定在虚表索引8的位置
    // 所有实现该接口的对象，Present函数都在这个位置（如同说明书第8页固定是"拍照功能"）
    MyPresent = (Present)VirtualTable[8];

    // 6.3 修改内存保护属性（让虚表可写）
    // 虚表默认是"只读"的（防止意外修改），需改为"可读可写可执行"才能修改
    DWORD oldProtect;
    VirtualProtect(VirtualTable, 1, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 6.4 替换虚表中的Present函数地址（完成Hook）
    // 关键原理3：修改全局共享虚表后，所有使用该接口的对象（包括游戏的交换链）
    // 调用Present时都会执行我们的VtPresent函数（如同修改官方说明书第8页，所有同型号手机都受影响）
    VirtualTable[8] = (DWORD64)VtPresent;

    return 0;
}
    
```

## 16. 16.ImGui-绘制内部窗口

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151803092
- Description: æç« æµè§éè¯»488æ¬¡ï¼ç¹èµ2æ¬¡ï¼æ¶è4æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui èè¡¨_imguiæ³¨å¥

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：15.ImGui-DX11虚表hook（二）-实现hook虚表dx11 
本次的代码绘制的窗口无法修改大小，这个是因为无Windows消息循环，游戏窗口分辨率改变会闪退 
如下图绘制内部窗口 
 
主要修改

删除的代码

完整代码

```text
// 包含必要头文件（DirectX、Windows API、ImGui等功能定义）
#include "main.h"

// 1. 获取Unreal引擎游戏窗口句柄（目标窗口）
// FindWindowA参数1："UnrealWindow"是Unreal引擎游戏的标准窗口类名（如《堡垒之夜》《艾尔登法环》等）
// 参数2：NULL表示匹配该类下的任意窗口（不限制窗口标题）
// 作用：后续ImGui界面会绘制到这个游戏窗口上
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量，用于渲染和ImGui初始化）
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建渲染资源（如ImGui的顶点缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（绘制ImGui界面）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：用于获取虚函数表（Hook的关键）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 主渲染目标：ImGui绘制的目标区域（游戏窗口的后台缓冲区）
DWORD64* VirtaulTable; // 全局虚表指针：存储IDXGISwapChain接口的共享虚函数表地址

// 3. 定义Present函数类型（匹配DXGI标准）
// Present是交换链的"显示画面"函数，负责将后台绘制好的内容显示到屏幕
// 参数说明：
// - This：调用该函数的交换链对象（游戏的交换链实例）
// - SyncInterval：垂直同步参数（0=关闭，1=开启，避免画面撕裂）
// - Flags：显示控制标志（通常为0）
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
);
Present MyPresent; // 存储游戏原始的Present函数地址（Hook后需调用，否则游戏画面无法显示）

// 4. 最终的Hook函数（每帧执行，用于绘制ImGui界面）
// 当游戏调用Present显示画面时，会先执行此函数，绘制完UI后再显示游戏画面
HRESULT VtPresent(
    IDXGISwapChain* This,  // 游戏的交换链对象（当前正在显示画面的交换链）
    UINT SyncInterval,     // 游戏的垂直同步设置
    UINT Flags             // 游戏的显示标志
) {
    // 4.1 开始ImGui新帧（每帧必须调用，初始化ImGui的内部状态）
    ImGui_ImplDX11_NewFrame();  // DX11后端新帧初始化
    ImGui_ImplWin32_NewFrame(); // Win32后端新帧初始化（处理输入如鼠标键盘）
    ImGui::NewFrame();          // ImGui核心新帧初始化

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：15.ImGui-DX11虚表hook（二）-实现hook虚表dx11 
本次的代码绘制的窗口无法修改大小，这个是因为无Windows消息循环，游戏窗口分辨率改变会闪退 
如下图绘制内部窗口 
 
主要修改 

 
 
 
 
删除的代码 

 
 
完整代码 

```text
// 包含必要头文件（DirectX、Windows API、ImGui等功能定义）
#include "main.h"

// 1. 获取Unreal引擎游戏窗口句柄（目标窗口）
// FindWindowA参数1："UnrealWindow"是Unreal引擎游戏的标准窗口类名（如《堡垒之夜》《艾尔登法环》等）
// 参数2：NULL表示匹配该类下的任意窗口（不限制窗口标题）
// 作用：后续ImGui界面会绘制到这个游戏窗口上
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量，用于渲染和ImGui初始化）
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建渲染资源（如ImGui的顶点缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（绘制ImGui界面）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：用于获取虚函数表（Hook的关键）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 主渲染目标：ImGui绘制的目标区域（游戏窗口的后台缓冲区）
DWORD64* VirtaulTable; // 全局虚表指针：存储IDXGISwapChain接口的共享虚函数表地址

// 3. 定义Present函数类型（匹配DXGI标准）
// Present是交换链的"显示画面"函数，负责将后台绘制好的内容显示到屏幕
// 参数说明：
// - This：调用该函数的交换链对象（游戏的交换链实例）
// - SyncInterval：垂直同步参数（0=关闭，1=开启，避免画面撕裂）
// - Flags：显示控制标志（通常为0）
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
);
Present MyPresent; // 存储游戏原始的Present函数地址（Hook后需调用，否则游戏画面无法显示）

// 4. 最终的Hook函数（每帧执行，用于绘制ImGui界面）
// 当游戏调用Present显示画面时，会先执行此函数，绘制完UI后再显示游戏画面
HRESULT VtPresent(
    IDXGISwapChain* This,  // 游戏的交换链对象（当前正在显示画面的交换链）
    UINT SyncInterval,     // 游戏的垂直同步设置
    UINT Flags             // 游戏的显示标志
) {
    // 4.1 开始ImGui新帧（每帧必须调用，初始化ImGui的内部状态）
    ImGui_ImplDX11_NewFrame();  // DX11后端新帧初始化
    ImGui_ImplWin32_NewFrame(); // Win32后端新帧初始化（处理输入如鼠标键盘）
    ImGui::NewFrame();          // ImGui核心新帧初始化

    // 4.2 定义ImGui界面（这里创建一个标题为"Hello, world!"的窗口）
    ImGui::Begin("Hello, world!");  // 开始创建窗口
    // 可在此处添加其他控件，如按钮：ImGui::Button("Click me!");
    ImGui::End();                   // 结束窗口创建

    // 4.3 渲染ImGui界面（生成绘制命令）
    ImGui::Render();
    // 设置渲染目标为游戏的后台缓冲区（告诉GPU：ImGui画到这个区域）
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    // 执行绘制命令，将ImGui界面画到游戏窗口上
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    // 4.4 调用游戏原始的Present函数（显示游戏画面，必须调用）
    return MyPresent(This, SyncInterval, Flags);
}

// 5. 初始化钩子函数（只执行一次，用于准备ImGui环境）
// 第一次调用Present时执行，完成初始化后会将Hook替换为VtPresent
HRESULT Init(
    IDXGISwapChain* This,  // 游戏的交换链对象（从这里获取游戏的渲染资源）
    UINT SyncInterval,     // 游戏的垂直同步设置
    UINT Flags             // 游戏的显示标志
) {
    // 5.1 获取游戏的DirectX设备和设备上下文
    // 从游戏的交换链中获取设备（This是游戏自己的交换链，不是我们创建的临时交换链）
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    // 从设备中获取设备上下文（用于后续绘制ImGui）
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    // 5.2 创建ImGui的渲染目标（绑定到游戏的后台缓冲区）
    ID3D11Texture2D* pBackBuffer; // 临时指针：游戏交换链的后台缓冲区
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer)); // 获取后台缓冲区
    // 用后台缓冲区创建渲染目标视图（告诉ImGui：画到游戏的这个缓冲区上）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release(); // 释放临时指针（渲染目标已引用该缓冲区）

    // 5.3 初始化ImGui（创建上下文、设置风格、绑定后端）
    ImGui::CreateContext();               // 创建ImGui核心上下文（管理UI状态）
    ImGui::StyleColorsDark();             // 设置UI风格为暗色主题
    ImGui_ImplWin32_Init(hWnd);           // 绑定Win32后端（处理游戏窗口的输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext); // 绑定DX11后端（用游戏的设备绘制）

    printf("初始化完成，已成功Hook游戏！\n"); // 打印日志，提示初始化完成

    // 5.4 将Hook从Init替换为VtPresent（初始化只做一次，后续交给VtPresent处理每帧UI）
    VirtaulTable[8] = (DWORD64)VtPresent;

    // 调用原始Present函数（显示当前帧画面）
    return MyPresent(This, SyncInterval, Flags);
}

// 6. 线程函数（核心：创建临时交换链，安装初始Hook）
// 该线程会在DLL注入游戏后启动，负责完成Hook的准备工作
DWORD Go(LPVOID lpThreadParameter) {
    // 6.1 配置临时交换链的参数（创建符合DXGI标准的交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd)); // 清空参数，避免随机值导致错误
    sd.BufferCount = 2;          // 双缓冲区（避免画面闪烁）
    sd.BufferDesc.Width = 0;     // 宽度自动匹配游戏窗口
    sd.BufferDesc.Height = 0;    // 高度自动匹配游戏窗口
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM; // 32位RGBA颜色格式（游戏通用）
    sd.BufferDesc.RefreshRate.Numerator = 60; // 目标刷新率60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH; // 允许窗口/全屏切换
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 缓冲区用于显示画面
    sd.OutputWindow = hWnd;      // 绑定到游戏窗口（确保交换链符合游戏窗口参数）
    sd.SampleDesc.Count = 1;     // 无抗锯齿（性能优先）
    sd.Windowed = TRUE;          // 窗口模式
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD; // 交换后丢弃后台数据（性能最优）

    // 6.2 创建临时的DirectX设备和交换链（用于获取虚函数表）
    UINT createDeviceFlags = 0;
    D3D_FEATURE_LEVEL featureLevel; // 存储实际支持的DirectX版本
    // 优先使用DX11.0，不支持则降级到DX10.0（兼容多数显卡）
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );
    // 若硬件加速失败，尝试软件渲染（兼容老显卡）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );
    if (res != S_OK) return false; // 若创建失败，退出线程

    // 6.3 获取IDXGISwapChain的全局共享虚表（关键步骤）
    // 所有IDXGISwapChain实例（包括游戏的和我们的临时交换链）共用此虚表
    VirtaulTable = *(DWORD64**)g_pSwapChain;

    // 6.4 保存原始Present函数地址（虚表第8位，微软标准规定）
    MyPresent = (Present)VirtaulTable[8];

    // 6.5 修改虚表内存保护（默认只读，需改为可写才能替换函数）
    DWORD oldProtect; // 存储原始内存保护属性
    VirtualProtect(
        VirtaulTable,    // 要修改的内存地址（虚表地址）
        1,               // 修改的字节数（1个函数地址足够）
        PAGE_EXECUTE_READWRITE, // 新属性：可读可写可执行
        &oldProtect      // 输出原始属性（此处无需恢复）
    );

    // 6.6 安装初始Hook：将Present函数替换为Init（第一次调用Present时执行初始化）
    VirtaulTable[8] = (DWORD64)Init;

    return 0; // 线程初始化完成
}
    

```

## 17. 17.ImGui-Hook消息循环

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151836224
- Description: æç« æµè§éè¯»475æ¬¡ï¼ç¹èµ4æ¬¡ï¼æ¶è5æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui hookæ¶æ¯å¾ªç¯_imgui setwindowlongptra é®é¢

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：16.ImGui-绘制内部窗口 
下图红框是ImGui里实现消息循环的代码，然后我们想得到游戏中的操作，比如改变窗口大小、键盘上按下了什么键，鼠标的操作等，就要得到游戏的消息循环，如果我们像下图一样创建一个消息循环，我们创建的消息循环只能得到，我们创建的窗口中的操作，没办法得到游戏中的操作，所以要获取一下游戏中的消息循环（获取的方式就是hook游戏的消息循环） 
 
hook消息循环的代码，如下图红框，使用 SetWindowLongPtrA 函数，这是微软提供的它可以替换原本窗口的消息处理函数，也就是把原本的消息循环替换成我们的消息循环 
 
然后找到ImGui的消息处理函数，如下图红框WndProc 
 
把下图红框的代码复制到我们的代码中 
 
如下图红框复制完后 
 
然后ImGui的消息处理函数返回的是 DefWindowProcW 这个函数的结果 
 
然后SetWindowLongPtr 微软官网说明要使用CallWindowProc函数，所以要改一下 
 
然后改完之后的代码 
 
效果图：我们的ImGui窗口就可以拖动、改变大小了，也就是能得到消息循环了 
 
完整代码和说明

```text
// 包含核心头文件：定义DirectX、Windows API、ImGui等基础功能
#include "main.h"

// 1. 获取游戏窗口句柄（定位目标窗口）
// 原理：Unreal引擎游戏的窗口类名固定为"UnrealWindow"（引擎官方定义）
// 作用：后续所有UI绘制和消息处理都绑定到这个窗口
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量）
// 为什么用static？确保变量在DLL生命周期内唯一，避免重复创建
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建ImGui所需的渲染资源
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行实际的绘制命令
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：仅用于获取Present函数的位置
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：绑定游戏后台缓冲区（UI绘制的目标）
DWORD64* VirtaulTable; // 虚函数表指针：存储IDXGISwapChain的全局共享函数表

// 3. 定义Present函数类型（遵循DXGI标准）
// 为什么这样定义？Present是交换链用于显示画面的核心函数，必须严格匹配其参数格式
// 参数说明：
// - This：调用该函数的交换链对象（游戏自身的交换链）
// - SyncInterval：垂直同步参数（0=关闭，1=开启）
// - Flags：显示控制标志（通常为0）
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
);
Present MyPresent; // 保存游戏原始的Present函数地址（Hook后需调用以显示画面）

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：16.ImGui-绘制内部窗口 
下图红框是ImGui里实现消息循环的代码，然后我们想得到游戏中的操作，比如改变窗口大小、键盘上按下了什么键，鼠标的操作等，就要得到游戏的消息循环，如果我们像下图一样创建一个消息循环，我们创建的消息循环只能得到，我们创建的窗口中的操作，没办法得到游戏中的操作，所以要获取一下游戏中的消息循环（获取的方式就是hook游戏的消息循环） 
 
hook消息循环的代码，如下图红框，使用 SetWindowLongPtrA 函数，这是微软提供的它可以替换原本窗口的消息处理函数，也就是把原本的消息循环替换成我们的消息循环 
 
然后找到ImGui的消息处理函数，如下图红框WndProc 
 
把下图红框的代码复制到我们的代码中 
 
如下图红框复制完后 
 
然后ImGui的消息处理函数返回的是 DefWindowProcW 这个函数的结果 
 
然后SetWindowLongPtr 微软官网说明要使用CallWindowProc函数，所以要改一下 
 
然后改完之后的代码 
 
效果图：我们的ImGui窗口就可以拖动、改变大小了，也就是能得到消息循环了 
 
完整代码和说明 

```text
// 包含核心头文件：定义DirectX、Windows API、ImGui等基础功能
#include "main.h"

// 1. 获取游戏窗口句柄（定位目标窗口）
// 原理：Unreal引擎游戏的窗口类名固定为"UnrealWindow"（引擎官方定义）
// 作用：后续所有UI绘制和消息处理都绑定到这个窗口
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量）
// 为什么用static？确保变量在DLL生命周期内唯一，避免重复创建
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建ImGui所需的渲染资源
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行实际的绘制命令
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：仅用于获取Present函数的位置
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：绑定游戏后台缓冲区（UI绘制的目标）
DWORD64* VirtaulTable; // 虚函数表指针：存储IDXGISwapChain的全局共享函数表

// 3. 定义Present函数类型（遵循DXGI标准）
// 为什么这样定义？Present是交换链用于显示画面的核心函数，必须严格匹配其参数格式
// 参数说明：
// - This：调用该函数的交换链对象（游戏自身的交换链）
// - SyncInterval：垂直同步参数（0=关闭，1=开启）
// - Flags：显示控制标志（通常为0）
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
);
Present MyPresent; // 保存游戏原始的Present函数地址（Hook后需调用以显示画面）

// 4. 最终Hook函数（每帧执行，绘制ImGui UI）
// 作用：替换游戏的Present函数，在显示画面时叠加ImGui界面
HRESULT VtPresent(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
) {
    // 初始化ImGui新帧（每帧必须调用，重置UI状态）
    // 为什么要分三步？ImGui需要先初始化后端（DX11/Win32），再初始化核心逻辑
    ImGui_ImplDX11_NewFrame();  // DX11后端初始化
    ImGui_ImplWin32_NewFrame(); // Win32后端初始化（处理输入）
    ImGui::NewFrame();          // ImGui核心初始化

    // 绘制ImGui窗口（示例：简单的Hello窗口）
    ImGui::Begin("Hello, world!");  // 开始创建窗口
    ImGui::End();                   // 结束窗口创建（必须与Begin配对）

    // 渲染ImGui界面（输出到游戏画面）
    ImGui::Render();
    // 绑定渲染目标：告诉GPU绘制到游戏的后台缓冲区
    // 为什么用g_mainRenderTargetView？它绑定了游戏的后台缓冲区，确保UI能叠加显示
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    // 执行绘制命令：将ImGui的UI数据画到屏幕上
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    // 调用游戏原始的Present函数（必须调用，否则游戏画面无法显示）
    return MyPresent(This, SyncInterval, Flags);
}

// 5. 窗口消息处理相关（让ImGui能响应鼠标/键盘）
// 声明ImGui的消息处理函数（来自ImGui库，负责处理UI交互）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC; // 保存游戏原始的窗口消息处理函数

// 自定义窗口消息处理函数（Hook游戏的消息处理）
// 作用：先让ImGui处理UI相关消息，再将剩余消息传给游戏
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 优先让ImGui处理消息（如UI拖动、按钮点击）
    // 为什么先处理？避免游戏误响应UI操作（如点击UI时游戏以为点击了游戏内物体）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 未被ImGui处理的消息，传给游戏原始函数（确保游戏正常响应操作）
    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}

// 6. 初始化Hook函数（只执行一次，准备ImGui环境）
// 作用：第一次调用Present时执行，完成初始化后切换到VtPresent
HRESULT Init(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
) {
    // Hook窗口消息处理函数（让ImGui能接收输入）
    // 为什么在这里Hook？初始化阶段只执行一次，确保UI显示前就具备交互能力
    myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc);
    
    // 获取游戏的DirectX设备和上下文（关键步骤）
    // 为什么从This获取？This是游戏自己的交换链，其绑定的设备与游戏环境完全兼容
    // 自己创建设备可能导致UI无法显示（设备不匹配）
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice);
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext);

    // 创建ImGui的渲染目标（绑定游戏后台缓冲区）
    // 为什么要绑定？ImGui必须画在游戏的缓冲区上才能与游戏画面叠加
    ID3D11Texture2D* pBackBuffer;
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer)); // 获取游戏的后台缓冲区
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView);
    pBackBuffer->Release(); // 释放临时指针（避免内存泄漏）

    // 初始化ImGui（创建上下文、绑定后端）
    ImGui::CreateContext();               // 创建ImGui核心上下文
    ImGui::StyleColorsDark();             // 设置暗色主题
    ImGui_ImplWin32_Init(hWnd);           // 绑定Win32后端（处理输入）
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext); // 绑定DX11后端（绘制UI）

    printf("HOOK成功：初始化完成\n"); // 调试日志

    // 切换Hook目标：从Init换成VtPresent（初始化完成，后续每帧执行VtPresent）
    VirtaulTable[8] = (DWORD64)VtPresent;

    // 调用原始Present函数（显示当前帧画面，避免黑屏）
    return MyPresent(This, SyncInterval, Flags);
}

// 7. 线程函数（核心：创建临时交换链，安装初始Hook）
// 为什么用线程？避免阻塞游戏主线程，确保注入后游戏能正常运行
DWORD Go(LPVOID lpThreadParameter) {
    // 配置临时交换链参数（创建符合游戏窗口特性的交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd)); // 清空参数（避免随机值导致创建失败）
    sd.BufferCount = 2;          // 双缓冲区（标准配置，避免画面闪烁）
    sd.BufferDesc.Width = 0;     // 宽度自动匹配游戏窗口
    sd.BufferDesc.Height = 0;    // 高度自动匹配游戏窗口
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM; // 32位RGBA（游戏通用格式）
    sd.BufferDesc.RefreshRate.Numerator = 60; // 刷新率60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH; // 允许窗口/全屏切换
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 用于显示画面
    sd.OutputWindow = hWnd;      // 绑定游戏窗口
    sd.SampleDesc.Count = 1;     // 无抗锯齿（性能优先）
    sd.Windowed = TRUE;          // 窗口模式（兼容性更好）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD; // 交换后丢弃后台数据（性能最优）

    // 创建临时DirectX设备和交换链（用于获取虚函数表）
    UINT createDeviceFlags = 0;
    D3D_FEATURE_LEVEL featureLevel;
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );
    // 硬件加速失败时，尝试软件渲染（兼容性兜底）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );
    if (res != S_OK) return false; // 创建失败则退出

    // 获取IDXGISwapChain的全局虚函数表（关键！所有交换链共用此表）
    VirtaulTable = *(DWORD64**)g_pSwapChain;

    // 保存原始Present函数地址（虚表第8位，微软标准规定）
    MyPresent = (Present)VirtaulTable[8];

    // 修改虚表内存保护（默认只读，需改为可写才能替换函数）
    DWORD oldProtect;
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &oldProtect);

    // 安装初始Hook：将Present替换为Init（第一次调用时执行初始化）
    VirtaulTable[8] = (DWORD64)Init;

    return 0;
}
    

```

## 18. 18.ImGui-解决修改分辨率闪退

- URL: https://jisuanjiwang.blog.csdn.net/article/details/151873539
- Description: æç« æµè§éè¯»449æ¬¡ï¼ç¹èµ4æ¬¡ï¼æ¶è7æ¬¡ãæ¸¸æéå æ¸¸æå®å¨ æ¸¸ææ»é² c++ åæ¸¸æå¤æ ä¿å§çº§æ»ç¥ Windows æ±ç¼ x64æ¸¸æ ImGui_imgui crash

### Summary

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：17.ImGui-Hook消息循环 
解决修改分辨率闪退问题需要hook下图红框里的函数，它也是交换链里的，需要在游戏调用ResizeBuffers函数之前把其它的东西释放掉，如果不进行释放在执行ResizeBuffers的时候就会导致闪退，它在虚函数表中第13的位置上 
 
跟之前book渲染函数Present一样，先写ResizeBuffers函数的声明，如下图红框 
 
然后再写一个我们自己的拦截函数，如下图红框 
 
然后写hook代码 
 
然后拦截的代码，也就是VtResizeBuffers函数中的逻辑，如下图红框 
 
VtResizeBuffers里把VirtaulTable[8]重新赋值成了Init函数，所以它又会来到Init函数，然后Init函数做了一下改动，让下图红框的代码只执行一次 
 
完整代码

```text
// 引入核心头文件：包含DirectX、Windows API、ImGui的基础功能定义
// 缺少此头文件，代码无法识别HWND、ID3D11Device等关键类型
#include "main.h"

// 1. 定位Unreal引擎游戏窗口（获取窗口句柄）
// 原理：Unreal引擎游戏的窗口类名固定为"UnrealWindow"（官方约定，如《艾尔登法环》《堡垒之夜》）
// 作用：后续ImGui绘制、窗口消息处理均绑定此窗口，确保操作目标正确
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量，生命周期与DLL一致）
// static修饰：确保变量唯一且仅当前文件可见，避免全局冲突
// 初始化为nullptr：防止未初始化的“野指针”导致崩溃
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建ImGui所需的渲染资源（如顶点缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（绘制ImGui界面）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：仅用于获取虚函数表（Hook关键）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：绑定游戏后台缓冲区（ImGui绘制目标）
DWORD64* VirtaulTable; // 全局虚函数表指针：存储IDXGISwapChain的共享函数表（所有交换链共用）

// 3. 定义ResizeBuffers函数类型（处理窗口缩放的核心函数）
// 为什么Hook？游戏窗口缩放（拖动边缘/切换全屏）时会调用此函数重置缓冲区
// 若不处理，ImGui绑定的旧缓冲区失效，会导致UI错位、黑屏
typedef HRESULT (STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,       // 调用者：游戏的交换链对象
    UINT BufferCount,           // 新缓冲区数量（通常为2，双缓冲）
    UINT Width,                 // 缩放后窗口宽度
    UINT Height,                // 缩放后窗口高度
    DXGI_FORMAT NewFormat,      // 新颜色格式（与原格式一致）
    UINT SwapChainFlags         // 交换链标志（保持原标志）
);
ResizeBuffers MyResizeBuffers; // 保存游戏原始的ResizeBuffers地址（缩放后需调用以重置游戏缓冲区）

### Full Content

免责声明：内容仅供学习参考，请合法利用知识，禁止进行违法犯罪活动！ 
本次游戏没法给 
内容参考于：微尘网络安全 
上一个内容：17.ImGui-Hook消息循环 
解决修改分辨率闪退问题需要hook下图红框里的函数，它也是交换链里的，需要在游戏调用ResizeBuffers函数之前把其它的东西释放掉，如果不进行释放在执行ResizeBuffers的时候就会导致闪退，它在虚函数表中第13的位置上 
 
跟之前book渲染函数Present一样，先写ResizeBuffers函数的声明，如下图红框 
 
然后再写一个我们自己的拦截函数，如下图红框 
 
然后写hook代码 
 
然后拦截的代码，也就是VtResizeBuffers函数中的逻辑，如下图红框 
 
VtResizeBuffers里把VirtaulTable[8]重新赋值成了Init函数，所以它又会来到Init函数，然后Init函数做了一下改动，让下图红框的代码只执行一次 
 
完整代码 

```text
// 引入核心头文件：包含DirectX、Windows API、ImGui的基础功能定义
// 缺少此头文件，代码无法识别HWND、ID3D11Device等关键类型
#include "main.h"

// 1. 定位Unreal引擎游戏窗口（获取窗口句柄）
// 原理：Unreal引擎游戏的窗口类名固定为"UnrealWindow"（官方约定，如《艾尔登法环》《堡垒之夜》）
// 作用：后续ImGui绘制、窗口消息处理均绑定此窗口，确保操作目标正确
HWND hWnd = FindWindowA("UnrealWindow", NULL);

// 2. DirectX11核心组件（全局变量，生命周期与DLL一致）
// static修饰：确保变量唯一且仅当前文件可见，避免全局冲突
// 初始化为nullptr：防止未初始化的“野指针”导致崩溃
static ID3D11Device* g_pd3dDevice = nullptr;               // 绘图设备：创建ImGui所需的渲染资源（如顶点缓冲区）
static ID3D11DeviceContext* g_pd3dDeviceContext = nullptr; // 设备上下文：执行渲染命令（绘制ImGui界面）
static IDXGISwapChain* g_pSwapChain = nullptr;             // 临时交换链：仅用于获取虚函数表（Hook关键）
static ID3D11RenderTargetView* g_mainRenderTargetView = nullptr; // 渲染目标：绑定游戏后台缓冲区（ImGui绘制目标）
DWORD64* VirtaulTable; // 全局虚函数表指针：存储IDXGISwapChain的共享函数表（所有交换链共用）

// 3. 定义ResizeBuffers函数类型（处理窗口缩放的核心函数）
// 为什么Hook？游戏窗口缩放（拖动边缘/切换全屏）时会调用此函数重置缓冲区
// 若不处理，ImGui绑定的旧缓冲区失效，会导致UI错位、黑屏
typedef HRESULT (STDMETHODCALLTYPE* ResizeBuffers)(
    IDXGISwapChain* This,       // 调用者：游戏的交换链对象
    UINT BufferCount,           // 新缓冲区数量（通常为2，双缓冲）
    UINT Width,                 // 缩放后窗口宽度
    UINT Height,                // 缩放后窗口高度
    DXGI_FORMAT NewFormat,      // 新颜色格式（与原格式一致）
    UINT SwapChainFlags         // 交换链标志（保持原标志）
);
ResizeBuffers MyResizeBuffers; // 保存游戏原始的ResizeBuffers地址（缩放后需调用以重置游戏缓冲区）

// 4. 自定义ResizeBuffers函数（窗口缩放时重置ImGui资源）
HRESULT VtResizeBuffers(
    IDXGISwapChain* This,
    UINT BufferCount,
    UINT Width,
    UINT Height,
    DXGI_FORMAT NewFormat,
    UINT SwapChainFlags
) {
    // 释放ImGui旧资源（为什么释放？）
    // 窗口缩放后，游戏后台缓冲区尺寸变化，旧渲染目标（g_mainRenderTargetView）已失效
    // 不释放会导致资源泄漏，且新资源无法绑定
    if (g_pd3dDevice) {
        g_pd3dDevice->Release();                  // 释放绘图设备
        g_pd3dDevice = nullptr;                   // 置空避免重复释放
        g_mainRenderTargetView->Release();        // 释放旧渲染目标
        g_mainRenderTargetView = nullptr;         // 置空避免重复释放
        ImGui_ImplDX11_Shutdown();                // 关闭ImGui的DX11后端（清理旧资源）
        VirtaulTable[8] = (DWORD64)Init;          // 切回Init函数：缩放后需重新初始化ImGui
    }

    // 调用游戏原始函数（必须调用！让游戏重置自身缓冲区，适应新窗口尺寸）
    return MyResizeBuffers(This, BufferCount, Width, Height, NewFormat, SwapChainFlags);
}

// 5. 定义Present函数类型（处理画面显示的核心函数）
// 为什么Hook？游戏每帧显示画面都会调用Present，替换后可叠加ImGui UI
typedef HRESULT(STDMETHODCALLTYPE* Present)(
    IDXGISwapChain* This,       // 调用者：游戏的交换链对象
    UINT SyncInterval,          // 垂直同步（0=关闭，1=开启）
    UINT Flags                  // 显示标志（通常为0）
);
Present MyPresent; // 保存游戏原始的Present地址（叠加UI后需调用以显示游戏画面）

// 6. 自定义Present函数（每帧绘制ImGui UI）
HRESULT VtPresent(
    IDXGISwapChain* This,
    UINT SyncInterval,
    UINT Flags
) {
    // ImGui帧初始化（每帧必须调用！重置UI状态）
    // 顺序不能乱：先初始化后端，再初始化核心
    ImGui_ImplDX11_NewFrame();  // DX11后端：准备渲染资源
    ImGui_ImplWin32_NewFrame(); // Win32后端：获取鼠标/键盘输入
    ImGui::NewFrame();          // ImGui核心：重置帧状态

    // 绘制ImGui窗口（示例：简单的Hello窗口）
    ImGui::Begin("Hello, world!");  // 开始创建窗口（标题为"Hello, world!"）
    ImGui::End();                   // 结束窗口创建（必须与Begin配对）

    // 渲染ImGui并输出到游戏窗口
    ImGui::Render(); // 生成绘制数据（将UI拆解为GPU可识别的顶点/颜色）
    // 绑定渲染目标：告诉GPU绘制到游戏后台缓冲区
    g_pd3dDeviceContext->OMSetRenderTargets(1, &g_mainRenderTargetView, nullptr);
    // 执行绘制：将ImGui画到屏幕上
    ImGui_ImplDX11_RenderDrawData(ImGui::GetDrawData());

    // 调用游戏原始函数（必须调用！否则游戏画面无法显示）
    return MyPresent(This, SyncInterval, Flags);
}

// 7. 窗口消息处理（让ImGui支持鼠标/键盘交互）
// 声明ImGui的消息处理函数（来自ImGui库，处理UI交互）
extern IMGUI_IMPL_API LRESULT ImGui_ImplWin32_WndProcHandler(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam);
WNDPROC myWNDPROC; // 保存游戏原始的消息处理函数（未处理的消息需传给游戏）

// 自定义消息处理函数（Hook游戏消息）
LRESULT WINAPI WndProc(HWND hWnd, UINT msg, WPARAM wParam, LPARAM lParam)
{
    // 优先让ImGui处理消息（为什么优先？）
    // 避免游戏误响应UI操作（如点击UI时，游戏不会以为是点击游戏内物体）
    if (ImGui_ImplWin32_WndProcHandler(hWnd, msg, wParam, lParam))
        return true;

    // 未被ImGui处理的消息（如游戏内移动、瞄准），传给游戏原始函数
    return ::CallWindowProc(myWNDPROC, hWnd, msg, wParam, lParam);
}

// 8. 初始化函数（仅执行一次，准备ImGui环境）
HRESULT Init(
    IDXGISwapChain* This,       // 游戏的交换链对象（获取兼容资源）
    UINT SyncInterval,          // 游戏的垂直同步设置
    UINT Flags                  // 游戏的显示标志
) {
    // 从游戏交换链获取渲染资源（为什么从游戏获取？）
    // 游戏的交换链绑定了适配自身环境的设备，自己创建可能不兼容（导致UI无法显示）
    This->GetDevice(_uuidof(g_pd3dDevice), (void**)&g_pd3dDevice); // 获取绘图设备
    g_pd3dDevice->GetImmediateContext((ID3D11DeviceContext**)&g_pd3dDeviceContext); // 获取设备上下文

    // 创建ImGui的渲染目标（绑定游戏后台缓冲区）
    ID3D11Texture2D* pBackBuffer; // 临时指针：存储游戏后台缓冲区
    This->GetBuffer(0, IID_PPV_ARGS(&pBackBuffer)); // 获取后台缓冲区（0=第一个缓冲区）
    g_pd3dDevice->CreateRenderTargetView(pBackBuffer, nullptr, &g_mainRenderTargetView); // 创建渲染目标
    pBackBuffer->Release(); // 释放临时指针（避免内存泄漏）

    // 初始化ImGui（static bool is：避免窗口缩放后重复初始化）
    static bool is = true;
    if (is) {
        is = false; // 置为false，后续缩放仅重新初始化DX11后端
        myWNDPROC = (WNDPROC)SetWindowLongPtrA(hWnd, GWLP_WNDPROC, (LONG_PTR)WndProc); // Hook窗口消息
        ImGui::CreateContext();               // 创建ImGui核心上下文
        ImGui::StyleColorsDark();             // 设置暗色主题
        ImGui_ImplWin32_Init(hWnd);           // 绑定Win32后端（处理输入）
    }
    
    ImGui_ImplDX11_Init(g_pd3dDevice, g_pd3dDeviceContext); // 初始化DX11后端（窗口缩放后需重新初始化）

    printf("HOOK初始化完成（支持窗口缩放）\n"); // 调试日志：确认初始化成功

    VirtaulTable[8] = (DWORD64)VtPresent; // 切到VtPresent：后续每帧绘制UI
    return MyPresent(This, SyncInterval, Flags); // 调用原始函数，避免初始化黑屏
}

// 9. 线程函数（核心：创建临时交换链，安装Hook）
// 为什么用线程？避免阻塞游戏主线程，确保注入后游戏正常运行
DWORD Go(LPVOID lpThreadParameter) {
    // 配置临时交换链参数（创建符合游戏窗口特性的交换链）
    DXGI_SWAP_CHAIN_DESC sd;
    ZeroMemory(&sd, sizeof(sd)); // 清空参数，避免随机值导致创建失败
    sd.BufferCount = 2;          // 双缓冲区（避免画面闪烁）
    sd.BufferDesc.Width = 0;     // 宽度自动匹配游戏窗口
    sd.BufferDesc.Height = 0;    // 高度自动匹配游戏窗口
    sd.BufferDesc.Format = DXGI_FORMAT_R8G8B8A8_UNORM; // 32位RGBA（游戏通用格式）
    sd.BufferDesc.RefreshRate.Numerator = 60; // 刷新率60Hz
    sd.BufferDesc.RefreshRate.Denominator = 1;
    sd.Flags = DXGI_SWAP_CHAIN_FLAG_ALLOW_MODE_SWITCH; // 允许窗口/全屏切换
    sd.BufferUsage = DXGI_USAGE_RENDER_TARGET_OUTPUT;  // 用于显示画面
    sd.OutputWindow = hWnd;      // 绑定游戏窗口
    sd.SampleDesc.Count = 1;     // 无抗锯齿（性能优先）
    sd.Windowed = TRUE;          // 窗口模式（兼容性更好）
    sd.SwapEffect = DXGI_SWAP_EFFECT_DISCARD; // 交换后丢弃后台数据（性能最优）

    // 创建临时DirectX设备和交换链（获取虚函数表的前提）
    UINT createDeviceFlags = 0;
    D3D_FEATURE_LEVEL featureLevel; // 存储实际支持的DirectX版本
    const D3D_FEATURE_LEVEL featureLevelArray[2] = { D3D_FEATURE_LEVEL_11_0, D3D_FEATURE_LEVEL_10_0 };
    HRESULT res = D3D11CreateDeviceAndSwapChain(
        nullptr, D3D_DRIVER_TYPE_HARDWARE, nullptr, createDeviceFlags,
        featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
        &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
    );

    // 硬件加速失败时，尝试软件渲染（兼容性兜底）
    if (res == DXGI_ERROR_UNSUPPORTED)
        res = D3D11CreateDeviceAndSwapChain(
            nullptr, D3D_DRIVER_TYPE_WARP, nullptr, createDeviceFlags,
            featureLevelArray, 2, D3D11_SDK_VERSION, &sd, &g_pSwapChain,
            &g_pd3dDevice, &featureLevel, &g_pd3dDeviceContext
        );
    if (res != S_OK) return false; // 创建失败则退出

    // 获取全局虚函数表（所有交换链共用此表）
    VirtaulTable = *(DWORD64**)g_pSwapChain;

    // Hook Present函数（初始指向Init，首次调用时初始化）
    MyPresent = (Present)VirtaulTable[8];
    DWORD oldProtect;
    VirtualProtect(VirtaulTable, 1, PAGE_EXECUTE_READWRITE, &oldProtect); // 虚表默认只读，需改为可写
    VirtaulTable[8] = (DWORD64)Init;

    // Hook ResizeBuffers函数（处理窗口缩放）
    MyResizeBuffers = (ResizeBuffers)VirtaulTable[13]; // 微软规定ResizeBuffers在虚表第13位
    VirtaulTable[13] = (DWORD64)VtResizeBuffers;

    return 0; // 线程初始化完成
}

```
