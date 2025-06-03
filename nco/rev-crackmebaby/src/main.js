const { app, BrowserWindow } = require("electron");
const path = require("path");

let mainWindow;

const createWindow = () => {
  mainWindow = new BrowserWindow({
    width: 300,
    height: 350,
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: false,
      devTools: false,
    },
  });
  mainWindow.setMenuBarVisibility(false);
  mainWindow.loadFile("index.html");
  mainWindow.webContents.openDevTools();
};

app.whenReady().then(() => {
  app.allowRendererProcessReuse = false;
  createWindow();
  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
