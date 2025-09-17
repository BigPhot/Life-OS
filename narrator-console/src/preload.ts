// See the Electron documentation for details on how to use preload scripts:
// https://www.electronjs.org/docs/latest/tutorial/process-model#preload-scripts

import { contextBridge, ipcRenderer } from 'electron';

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // Example IPC methods - to be expanded later
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  saveFile: (data: any) => ipcRenderer.invoke('dialog:saveFile', data),

  // App lifecycle methods
  minimize: () => ipcRenderer.invoke('app:minimize'),
  maximize: () => ipcRenderer.invoke('app:maximize'),
  close: () => ipcRenderer.invoke('app:close'),

  // Data methods - to be implemented later
  loadData: () => ipcRenderer.invoke('data:load'),
  saveData: (data: any) => ipcRenderer.invoke('data:save', data),
});

// Type declaration for the exposed API
declare global {
  interface Window {
    electronAPI: {
      openFile: () => Promise<any>;
      saveFile: (data: any) => Promise<any>;
      minimize: () => Promise<void>;
      maximize: () => Promise<void>;
      close: () => Promise<void>;
      loadData: () => Promise<any>;
      saveData: (data: any) => Promise<any>;
    };
  }
}