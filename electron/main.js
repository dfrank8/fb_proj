const electron = require('electron')
const { app, BrowserWindow } = electron
const path = require('path')
const url = require('url')
const io = require('socket.io-client');
const socket = io('http://localhost:8090/');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win;


function createWindow() {
    // Create the browser window.
  const display = electron.screen.getPrimaryDisplay();
    win = new BrowserWindow({
      x: 0,
      y: 0,
      height: 1,
      width: 1,
      transparent: false,
      movable: true,
      minimizable: false,
      maximizable: false,
      useContentSize: true,
      resizeable: true,
      alwaysOnTop: false,
      fullscreenable: false,
      frame: false,
      hasShadow: false,
    })
    // and load the index.html of the app.
    win.loadURL('http://localhost:7001/')

    // Open the DevTools.
    //win.webContents.openDevTools()
    win.setResizable(true);
    // win.setBounds(bounds[, animate])
    // win.setBounds({ 'x': 0, 'y': 0, 'width': 100, 'height': 100 });
    // win.focus();

    // Emitted when the window is closed.
    win.on('closed', () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        win = null
    })
}

socket.on('connect', (socket) => {
    console.log('a user connected');
});
socket.on('disconnect', () => {
    console.log('user disconnected');
});

socket.on('hide_window', () => {
    console.log('hide window');
});

socket.on('window', (data) => {
  console.log('window >>> ', data);
  if (data == "show") {
    win.setSize(800,700,true);
  } else if (data == "hide") {
    win.setSize(1,1,true);
  }
  // socket.join(data.room);
});

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow)

// // Quit when all windows are closed.
// app.on('window-all-closed', () => {
//   // On macOS it is common for applications and their menu bar
//   // to stay active until the user quits explicitly with Cmd + Q
//   // if (process.platform !== 'darwin') {
//   //   app.quit()
//   // }
// })

// app.on('activate', () => {
//   // On macOS it's common to re-create a window in the app when the
//   // dock icon is clicked and there are no other windows open.
//   if (win === null) {
//     createWindow()
//   }
// })

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
