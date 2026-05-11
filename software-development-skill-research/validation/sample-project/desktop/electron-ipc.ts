import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("orders", {
  exportCsv: (accountId: string) => {
    if (!/^[a-zA-Z0-9_-]+$/.test(accountId)) {
      throw new Error("Invalid account id");
    }
    return ipcRenderer.invoke("orders:exportCsv", { accountId });
  },
});
