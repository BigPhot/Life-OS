"use strict";
const electron = require("electron");
electron.contextBridge.exposeInMainWorld("electronAPI", {
  // Example IPC methods - to be expanded later
  openFile: () => electron.ipcRenderer.invoke("dialog:openFile"),
  saveFile: (data) => electron.ipcRenderer.invoke("dialog:saveFile", data),
  // App lifecycle methods
  minimize: () => electron.ipcRenderer.invoke("app:minimize"),
  maximize: () => electron.ipcRenderer.invoke("app:maximize"),
  close: () => electron.ipcRenderer.invoke("app:close"),
  // Data methods - to be implemented later
  loadData: () => electron.ipcRenderer.invoke("data:load"),
  saveData: (data) => electron.ipcRenderer.invoke("data:save", data)
});
//# sourceMappingURL=index.js.map
