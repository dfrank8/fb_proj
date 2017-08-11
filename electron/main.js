const electron = require('electron')
const { app, BrowserWindow } = electron
const path = require('path')
const url = require('url')
const io = require('socket.io-client');
const socket = io('http://localhost:8090/');
const FB = require('fb');
const ioHook = require('iohook');

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
let win;
var comboDict = {
    29: false,
    42: false,
    33: false
};

ioHook.on("keydown", event => {
    // console.log(event["keycode"])
    if(event["keycode"] == 1)
    {
        win.setSize(1, 800, true);
        return;
    }
    if (event["keycode"] in comboDict) {
        comboDict[event["keycode"]] = true;
    }
    combo = true;
    for (var key in comboDict) {
        // console.log(key)
        if (comboDict[key] == false) {
            // console.log(key + " is false")
            combo = false;
        }
    }
    if (combo) {
        win.setSize(800, 700, true);
    }
});

ioHook.on("keyup", event => {
    if (event["keycode"] in comboDict) {
        comboDict[event["keycode"]] = false;
    }
});

function createWindow() {
    // Create the browser window.
    const display = electron.screen.getPrimaryDisplay();
    win = new BrowserWindow({
        x: 0,
        y: 0,
        height: 800,
        width: 1,
        transparent: false,
        movable: false,
        minimizable: false,
        maximizable: false,
        useContentSize: true,
        resizeable: false,
        alwaysOnTop: true,
        fullscreenable: false,
        frame: false,
        hasShadow: true,
    })
    // and load the index.html of the app.
    // Open the DevTools.
    win.loadURL('http://localhost:5000')
    win.webContents.openDevTools()
    // win.setBounds(bounds[, animate])
    // win.setBounds({ 'x': 0, 'y': 0, 'width': 100, 'height': 100 });
    win.focus();

}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', () => {
    createWindow();
    ioHook.start();
});
// // Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    app.quit()

})

// app.on('activate', () => {
//   // On macOS it's common to re-create a window in the app when the
//   // dock icon is clicked and there are no other windows open.
//   if (win === null) {
//     createWindow()
//   }
// })

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.