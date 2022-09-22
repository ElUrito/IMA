import gui
import wx


def main():
    app = wx.App()
    ex = gui.MyFrame(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()