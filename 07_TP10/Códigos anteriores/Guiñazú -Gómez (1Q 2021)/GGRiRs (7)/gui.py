import wx
import wx.xrc
import wx.grid
import wx.dataview
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import funciones
import os
import xlsxwriter
import csv

if not os.path.exists('temp'):
    os.makedirs('temp')

#Venata principal de la GUI
class MyFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"GGRiRs", pos=wx.DefaultPosition,
                          size=wx.Size(1100, 700), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        ico = wx.Icon('gg1.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)

        self.currentDirectory=os.getcwd()
        self.SetSizeHints(wx.Size(1100, 700), wx.Size(-1, -1))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.m_menubar3 = wx.MenuBar(0)
        self.m_menu3 = wx.Menu()
        self.m_menu2 = wx.Menu()
        self.m_menuItem8 = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Respuesta al Impulso", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuItem8)

        self.m_menuItem6 = wx.MenuItem(self.m_menu2, wx.ID_ANY, u"Sine Sweep Grabado", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu2.Append(self.m_menuItem6)

        self.m_menu3.AppendSubMenu(self.m_menu2, u"Importar")

        self.m_menu5 = wx.Menu()
        self.m_menuItem9 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"Excel(.xlsx)", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.m_menuItem9)

        self.m_menuItem10 = wx.MenuItem(self.m_menu5, wx.ID_ANY, u"CSV(.csv)", wx.EmptyString, wx.ITEM_NORMAL)
        self.m_menu5.Append(self.m_menuItem10)

        self.m_menu3.AppendSubMenu(self.m_menu5, u"Exportar")

        self.m_menuItem11 = wx.MenuItem(self.m_menu3, wx.ID_ANY, u"Salir" + u"\t" + u"Ctrl+E", wx.EmptyString,
                                        wx.ITEM_NORMAL)
        self.m_menu3.Append(self.m_menuItem11)

        self.m_menubar3.Append(self.m_menu3, u"Archivo")

        self.SetMenuBar(self.m_menubar3)
        self.m_dataViewListCtrl1 = wx.dataview.DataViewListCtrl(self, wx.ID_ANY, wx.DefaultPosition,
                                                                wx.Size(-1, -1), wx.dataview.DV_MULTIPLE)
        self.m_dataViewListCtrl1.Hide()
        self.m_dataViewListColumn2 = self.m_dataViewListCtrl1.AppendTextColumn(u"Mediciones")
        gSizer1 = wx.GridSizer(2, 0, 0, 0)

        self.m_panel8 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel8, wx.ID_ANY, u"Gráfico"), wx.VERTICAL)

        self.m_panel9 = wx.Panel(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                 wx.TAB_TRAVERSAL)

        sbSizer4.Add(self.m_panel9, 2, wx.EXPAND | wx.ALL, 5)

        self.m_panel8.SetSizer(sbSizer4)
        self.m_panel8.Layout()
        sbSizer4.Fit(self.m_panel8)
        gSizer1.Add(self.m_panel8, 2, wx.ALL | wx.EXPAND, 5)

        self.m_panel12 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)


        fgSizer6 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer6.AddGrowableCol(1)
        fgSizer6.SetFlexibleDirection(wx.BOTH)
        fgSizer6.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        sbSizer41 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel12, wx.ID_ANY, u"Parámetros"), wx.VERTICAL)


        bSizer161 = wx.BoxSizer(wx.VERTICAL)

        bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText10 = wx.StaticText(sbSizer41.GetStaticBox(), wx.ID_ANY, u"Metodo de suavizado",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText10.Wrap(-1)
        bSizer17.Add(self.m_staticText10, 1, wx.ALL | wx.EXPAND, 5)

        m_choice3Choices = [u"Integral de Schroeder", u"Mediana Movil"]
        self.m_choice3 = wx.Choice(sbSizer41.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                   m_choice3Choices, 0)
        self.m_choice3.SetSelection(0)
        bSizer17.Add(self.m_choice3, 1, wx.ALL, 5)

        bSizer161.Add(bSizer17, 1, wx.EXPAND, 5)

        bSizer181 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText11 = wx.StaticText(sbSizer41.GetStaticBox(), wx.ID_ANY, u"Tamaño de ventana de Mediana Movil (ms)",
                                            wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText11.Wrap(-1)
        bSizer181.Add(self.m_staticText11, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl7 = wx.TextCtrl(sbSizer41.GetStaticBox(), wx.ID_ANY,u"50", wx.DefaultPosition,
                                       wx.DefaultSize, 0)
        self.m_textCtrl7.Enable(False)
        bSizer181.Add(self.m_textCtrl7, 1, wx.ALL, 5)

        bSizer161.Add(bSizer181, 1, wx.EXPAND, 5)

        sbSizer41.Add(bSizer161, 2, wx.EXPAND, 5)

        self.m_button3 = wx.Button(sbSizer41.GetStaticBox(), wx.ID_ANY, u"Generar Filtro Inverso", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        self.m_button3.Enable(False)
        sbSizer41.Add(self.m_button3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_button5 = wx.Button(sbSizer41.GetStaticBox(), wx.ID_ANY, u"Calcular Parametros", wx.DefaultPosition,
                                   wx.DefaultSize, 0)
        sbSizer41.Add(self.m_button5, 1, wx.ALL | wx.EXPAND, 5)

        fgSizer6.Add(sbSizer41, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel12, wx.ID_ANY, u"Resultados"), wx.VERTICAL)

        self.m_notebook1 = wx.Notebook(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_panel51 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer2 = wx.BoxSizer(wx.VERTICAL)
        self.m_panel51.SetMinSize((1000,1000))

        self.m_grid2 = wx.grid.Grid(self.m_panel51, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid2.CreateGrid(8, 10)
        self.m_grid2.EnableEditing(False)
        self.m_grid2.EnableGridLines(True)
        self.m_grid2.EnableDragGridSize(True)
        self.m_grid2.SetMargins(0, 0)

        # Columns

        self.m_grid2.EnableDragColMove(False)
        self.m_grid2.EnableDragColSize(True)
        self.m_grid2.SetColLabelSize(30)
        self.m_grid2.SetColLabelValue(0, u"31,5")
        self.m_grid2.SetColLabelValue(1, u"63")
        self.m_grid2.SetColLabelValue(2, u"125")
        self.m_grid2.SetColLabelValue(3, u"250")
        self.m_grid2.SetColLabelValue(4, u"500")
        self.m_grid2.SetColLabelValue(5, u"1k")
        self.m_grid2.SetColLabelValue(6, u"2k")
        self.m_grid2.SetColLabelValue(7, u"4k")
        self.m_grid2.SetColLabelValue(8, u"8k")
        self.m_grid2.SetColLabelValue(9, u"16k")
        self.m_grid2.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid2.SetRowSize(0, 19)
        self.m_grid2.SetRowSize(1, 19)
        self.m_grid2.SetRowSize(2, 19)
        self.m_grid2.SetRowSize(3, 19)
        self.m_grid2.SetRowSize(4, 19)
        self.m_grid2.SetRowSize(5, 19)
        self.m_grid2.SetRowSize(6, 19)
        self.m_grid2.SetRowSize(7, 19)
        self.m_grid2.AutoSizeRows()
        self.m_grid2.EnableDragRowSize(True)
        self.m_grid2.SetRowLabelSize(80)

        self.m_grid2.SetRowLabelValue(0, u"EDT(s)")
        self.m_grid2.SetRowLabelValue(1, u"RT20(s)")
        self.m_grid2.SetRowLabelValue(2, u"RT30(s)")
        self.m_grid2.SetRowLabelValue(3, u"IACC Early")
        self.m_grid2.SetRowLabelValue(4, u"C50(dB)")
        self.m_grid2.SetRowLabelValue(5, u"C80(dB)")
        self.m_grid2.SetRowLabelValue(6, u"Tt(ms)")
        self.m_grid2.SetRowLabelValue(7, u"EDTt(s)")
        self.m_grid2.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid2.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer2.Add(self.m_grid2, 1, wx.ALL, 5)

        self.m_panel51.SetSizer(bSizer2)
        self.m_panel51.Layout()
        bSizer2.Fit(self.m_panel51)
        self.m_notebook1.AddPage(self.m_panel51, u"Octavas", True)
        self.m_panel6 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_grid1 = wx.grid.Grid(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid1.CreateGrid(8, 30)
        self.m_grid1.EnableEditing(False)
        self.m_grid1.EnableGridLines(True)
        self.m_grid1.EnableDragGridSize(True)
        self.m_grid1.SetMargins(0, 0)

        # Columns

        self.m_grid1.EnableDragColMove(False)
        self.m_grid1.EnableDragColSize(True)
        self.m_grid1.SetColLabelSize(30)
        self.m_grid1.SetColLabelValue(0, u"25")
        self.m_grid1.SetColLabelValue(1, u"31,5")
        self.m_grid1.SetColLabelValue(2, u"40")
        self.m_grid1.SetColLabelValue(3, u"50")
        self.m_grid1.SetColLabelValue(4, u"63")
        self.m_grid1.SetColLabelValue(5, u"80")
        self.m_grid1.SetColLabelValue(6, u"100")
        self.m_grid1.SetColLabelValue(7, u"125")
        self.m_grid1.SetColLabelValue(8, u"160")
        self.m_grid1.SetColLabelValue(9, u"200")
        self.m_grid1.SetColLabelValue(10, u"250")
        self.m_grid1.SetColLabelValue(11, u"315")
        self.m_grid1.SetColLabelValue(12, u"400")
        self.m_grid1.SetColLabelValue(13, u"500")
        self.m_grid1.SetColLabelValue(14, u"630")
        self.m_grid1.SetColLabelValue(15, u"800")
        self.m_grid1.SetColLabelValue(16, u"1k")
        self.m_grid1.SetColLabelValue(17, u"1k25")
        self.m_grid1.SetColLabelValue(18, u"1k6")
        self.m_grid1.SetColLabelValue(19, u"2k")
        self.m_grid1.SetColLabelValue(20, u"2k5")
        self.m_grid1.SetColLabelValue(21, u"3k15")
        self.m_grid1.SetColLabelValue(22, u"4k")
        self.m_grid1.SetColLabelValue(23, u"5k")
        self.m_grid1.SetColLabelValue(24, u"6k3")
        self.m_grid1.SetColLabelValue(25, u"8k")
        self.m_grid1.SetColLabelValue(26, u"10k")
        self.m_grid1.SetColLabelValue(27, u"12k5")
        self.m_grid1.SetColLabelValue(28, u"16k")
        self.m_grid1.SetColLabelValue(29, u"20k")

        self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid1.SetRowSize(0, 19)
        self.m_grid1.SetRowSize(1, 19)
        self.m_grid1.SetRowSize(2, 19)
        self.m_grid1.SetRowSize(3, 19)
        self.m_grid1.SetRowSize(4, 19)
        self.m_grid1.SetRowSize(5, 19)
        self.m_grid1.SetRowSize(6, 19)
        self.m_grid1.SetRowSize(7, 19)
        self.m_grid1.AutoSizeRows()
        self.m_grid1.EnableDragRowSize(True)
        self.m_grid1.SetRowLabelSize(80)

        self.m_grid1.SetRowLabelValue(0, u"EDT(s)")
        self.m_grid1.SetRowLabelValue(1, u"RT20(s)")
        self.m_grid1.SetRowLabelValue(2, u"RT30(s)")
        self.m_grid1.SetRowLabelValue(3, u"IACC Early")
        self.m_grid1.SetRowLabelValue(4, u"C50(dB)")
        self.m_grid1.SetRowLabelValue(5, u"C80(dB)")
        self.m_grid1.SetRowLabelValue(6, u"Tt(ms)")
        self.m_grid1.SetRowLabelValue(7, u"EDTt(s)")
        self.m_grid1.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer3.Add(self.m_grid1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel6.SetSizer(bSizer3)
        self.m_panel6.Layout()
        bSizer3.Fit(self.m_panel6)
        self.m_notebook1.AddPage(self.m_panel6, u"Tercios de Octava", False)

        self.m_panel71 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)

        self.m_grid4 = wx.grid.Grid(self.m_panel71, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid4.CreateGrid(8, 10)
        self.m_grid4.EnableEditing(False)
        self.m_grid4.EnableGridLines(True)
        self.m_grid4.EnableDragGridSize(True)
        self.m_grid4.SetMargins(0, 0)

        # Columns

        self.m_grid4.EnableDragColMove(False)
        self.m_grid4.EnableDragColSize(True)
        self.m_grid4.SetColLabelSize(30)
        self.m_grid4.SetColLabelValue(0, u"31,5")
        self.m_grid4.SetColLabelValue(1, u"63")
        self.m_grid4.SetColLabelValue(2, u"125")
        self.m_grid4.SetColLabelValue(3, u"250")
        self.m_grid4.SetColLabelValue(4, u"500")
        self.m_grid4.SetColLabelValue(5, u"1k")
        self.m_grid4.SetColLabelValue(6, u"2k")
        self.m_grid4.SetColLabelValue(7, u"4k")
        self.m_grid4.SetColLabelValue(8, u"8k")
        self.m_grid4.SetColLabelValue(9, u"16k")
        self.m_grid4.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid4.SetRowSize(0, 19)
        self.m_grid4.SetRowSize(1, 19)
        self.m_grid4.SetRowSize(2, 19)
        self.m_grid4.SetRowSize(3, 19)
        self.m_grid4.SetRowSize(4, 19)
        self.m_grid4.SetRowSize(5, 19)
        self.m_grid4.SetRowSize(6, 19)
        self.m_grid4.SetRowSize(7, 19)
        self.m_grid4.AutoSizeRows()
        self.m_grid4.EnableDragRowSize(True)
        self.m_grid4.SetRowLabelSize(80)

        self.m_grid4.SetRowLabelValue(0, u"EDT(s)")
        self.m_grid4.SetRowLabelValue(1, u"RT20(s)")
        self.m_grid4.SetRowLabelValue(2, u"RT30(s)")
        self.m_grid4.SetRowLabelValue(3, u"IACC Early")
        self.m_grid4.SetRowLabelValue(4, u"C50(dB)")
        self.m_grid4.SetRowLabelValue(5, u"C80(dB)")
        self.m_grid4.SetRowLabelValue(6, u"Tt(ms)")
        self.m_grid4.SetRowLabelValue(7, u"EDTt(s)")
        self.m_grid4.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid4.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)
        bSizer6.Add(self.m_grid4, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel71.SetSizer(bSizer6)
        self.m_panel71.Layout()
        bSizer6.Fit(self.m_panel71)


        self.m_panel61 = wx.Panel(self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)



        self.m_grid3 = wx.grid.Grid(self.m_panel61, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid3.CreateGrid(8, 30)
        self.m_grid3.EnableEditing(False)
        self.m_grid3.EnableGridLines(True)
        self.m_grid3.EnableDragGridSize(True)
        self.m_grid3.SetMargins(0, 0)

        # Columns

        self.m_grid3.EnableDragColMove(False)
        self.m_grid3.EnableDragColSize(True)
        self.m_grid3.SetColLabelSize(30)
        self.m_grid3.SetColLabelValue(0, u"25")
        self.m_grid3.SetColLabelValue(1, u"31,5")
        self.m_grid3.SetColLabelValue(2, u"40")
        self.m_grid3.SetColLabelValue(3, u"50")
        self.m_grid3.SetColLabelValue(4, u"63")
        self.m_grid3.SetColLabelValue(5, u"80")
        self.m_grid3.SetColLabelValue(6, u"100")
        self.m_grid3.SetColLabelValue(7, u"125")
        self.m_grid3.SetColLabelValue(8, u"160")
        self.m_grid3.SetColLabelValue(9, u"200")
        self.m_grid3.SetColLabelValue(10, u"250")
        self.m_grid3.SetColLabelValue(11, u"315")
        self.m_grid3.SetColLabelValue(12, u"400")
        self.m_grid3.SetColLabelValue(13, u"500")
        self.m_grid3.SetColLabelValue(14, u"630")
        self.m_grid3.SetColLabelValue(15, u"800")
        self.m_grid3.SetColLabelValue(16, u"1k")
        self.m_grid3.SetColLabelValue(17, u"1k25")
        self.m_grid3.SetColLabelValue(18, u"1k6")
        self.m_grid3.SetColLabelValue(19, u"2k")
        self.m_grid3.SetColLabelValue(20, u"2k5")
        self.m_grid3.SetColLabelValue(21, u"3k15")
        self.m_grid3.SetColLabelValue(22, u"4k")
        self.m_grid3.SetColLabelValue(23, u"5k")
        self.m_grid3.SetColLabelValue(24, u"6k3")
        self.m_grid3.SetColLabelValue(25, u"8k")
        self.m_grid3.SetColLabelValue(26, u"10k")
        self.m_grid3.SetColLabelValue(27, u"12k5")
        self.m_grid3.SetColLabelValue(28, u"16k")
        self.m_grid3.SetColLabelValue(29, u"20k")

        self.m_grid3.SetColLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Rows
        self.m_grid3.SetRowSize(0, 19)
        self.m_grid3.SetRowSize(1, 19)
        self.m_grid3.SetRowSize(2, 19)
        self.m_grid3.SetRowSize(3, 19)
        self.m_grid3.SetRowSize(4, 19)
        self.m_grid3.SetRowSize(5, 19)
        self.m_grid3.SetRowSize(6, 19)
        self.m_grid3.SetRowSize(7, 19)
        self.m_grid3.AutoSizeRows()
        self.m_grid3.EnableDragRowSize(True)
        self.m_grid3.SetRowLabelSize(80)
        self.m_grid3.SetRowLabelValue(0, u"EDT(s)")
        self.m_grid3.SetRowLabelValue(1, u"RT20(s)")
        self.m_grid3.SetRowLabelValue(2, u"RT30(s)")
        self.m_grid3.SetRowLabelValue(3, u"IACC Early")
        self.m_grid3.SetRowLabelValue(4, u"C50(dB)")
        self.m_grid3.SetRowLabelValue(5, u"C80(dB)")
        self.m_grid3.SetRowLabelValue(6, u"Tt(ms)")
        self.m_grid3.SetRowLabelValue(7, u"EDTt(s)")
        self.m_grid3.SetRowLabelAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)

        # Label Appearance

        # Cell Defaults
        self.m_grid3.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)

        bSizer5 = wx.BoxSizer(wx.VERTICAL)
        bSizer5.Add(self.m_grid3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel61.SetSizer(bSizer5)
        self.m_panel61.Layout()
        bSizer5.Fit(self.m_panel61)

        self.m_grid3.Hide()
        self.m_panel61.Hide()
        self.m_panel71.Hide()
        self.m_grid4.Hide()

        sbSizer3.Add(self.m_notebook1, 1, wx.EXPAND | wx.ALL, 5)

        fgSizer6.Add(sbSizer3, 1, wx.ALL | wx.EXPAND, 5)

        self.m_panel12.SetSizer(fgSizer6)
        self.m_panel12.Layout()
        fgSizer6.Fit(self.m_panel12)
        gSizer1.Add(self.m_panel12, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(gSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.importarImpulso, id=self.m_menuItem8.GetId())
        self.Bind(wx.EVT_MENU, self.importarSine, id=self.m_menuItem6.GetId())
        self.Bind(wx.EVT_MENU, self.exportarExcel, id=self.m_menuItem9.GetId())
        self.Bind(wx.EVT_MENU, self.exportarCSV, id=self.m_menuItem10.GetId())
        self.Bind(wx.EVT_MENU, self.salir, id=self.m_menuItem11.GetId())
        self.Bind(wx.grid.EVT_GRID_COL_SORT, self.graficar, self.m_grid1)
        self.Bind(wx.grid.EVT_GRID_COL_SORT, self.graficar, self.m_grid2)
        self.Bind(wx.grid.EVT_GRID_COL_SORT, self.graficar, self.m_grid3)
        self.Bind(wx.grid.EVT_GRID_COL_SORT, self.graficar, self.m_grid4)
        self.Bind(wx.EVT_CHOICE, self.habilitar, self.m_choice3)
        self.m_button3.Bind(wx.EVT_BUTTON, self.abrirConfSine)
        self.m_button5.Bind(wx.EVT_BUTTON, self.calcularParametros)

    def __del__(self):
        pass


    # Función para abrir un archivo
    def abrirArchivo(self, event):
        wildcard = "wav (*.wav)|*.wav|" \
                   "All files (*.*)|*.*"
        """
        Create and show the Open FileDialog
        """
        self.m_grid3.Show()
        self.m_grid4.Show()
        dlg = wx.FileDialog(
            self, message="Elegir archivos",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard=wildcard,
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR
        )
        paths=[]

        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            self.m_dataViewListCtrl1.DeleteAllItems()
            for i in range(len(paths)):
                self.m_dataViewListCtrl1.AppendItem([paths[i]])

            self.m_dataViewListCtrl1.SelectAll()

        return paths

    #Función para importar Respuesta al impulso y ploteado
    def importarImpulso(self, e):

        paths=self.abrirArchivo(e) #Se abre el archivo

        paths = paths[0]

        self.fs, self.senial_promedio = funciones.promediado_seniales(paths) #Se extrae la data del archivo

        y = self.senial_promedio

        y = y[0]

        W, H = self.m_panel9.GetSize()

        px = 1 / plt.rcParams['figure.dpi']  # Se plotea le energía de la señal importada en la GUI
        fig = plt.figure(figsize=(W * px, H * px))
        ax = fig.add_subplot(111)
        x = np.arange(0, len(y) / self.fs, 1 / self.fs)
        E = 20 * np.log10(y)
        ax.plot(x, E)
        ax.set_xlabel('Tiempo [s]')
        ax.set_ylabel('dBFS')
        plt.tight_layout()
        try:
            self.canvas.Destroy()
        except:
            pass
        self.canvas = FigureCanvas(self.m_panel9, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 0)
        self.m_panel9.SetSizerAndFit(sizer)
        self.m_button3.Disable()


    #Función para importar Sine-gradado y ploteado
    def importarSine(self, e):
        self.m_button3.Enable(False)

        paths = self.abrirArchivo(e) #Se abre el archivo

        paths = paths[0]

        self.fs, self.senial_promedio = funciones.promediado_seniales(paths) #Se extrae la data de los archivos

        y = self.senial_promedio

        y = y[0]

        W, H = self.m_panel9.GetSize()

        px = 1 / plt.rcParams['figure.dpi']  #Se plotea el sine-sweep grabado
        fig = plt.figure(figsize=(W * px, H * px))
        ax = fig.add_subplot(111)
        x = np.arange(0, len(y) / self.fs, 1 / self.fs)
        ax.plot(x, y)
        ax.set_xlabel('Tiempo')
        ax.set_ylabel('Amplitud')
        plt.tight_layout()
        try:
            self.canvas.Destroy()
        except:
            pass
        self.canvas = FigureCanvas(self.m_panel9, -1, fig)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 0)
        self.m_panel9.SetSizerAndFit(sizer)
        self.m_button3.Enable()


    #Función para exportar los datos a excel
    def exportarExcel(self, event):

        wildcard = "Excel (.xlsx)|.xlsx"

        dialog = wx.FileDialog(
            self, message="Guardar archivo",
            defaultDir=self.currentDirectory,
            defaultFile="Datos Medición",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPath()

            workbook = xlsxwriter.Workbook(paths, {'nan_inf_to_errors': True})
            worksheet = workbook.add_worksheet()
            decimales = workbook.add_format({'num_format': '#,##0.000'})
            bordeynegrita = workbook.add_format({'bold': True, 'border':1})

            worksheet.write_row('B1', funciones.bandas_octavas,bordeynegrita)
            worksheet.write_column('A2', ["EDT(s)", "T20(s)", "T30(s)", "IACC early", "C50(dB)", "C80(dB)", "Tt(ms)",
                                          "EDTt(s)"],bordeynegrita)

            #Parametros Octavas L


            worksheet.write_row('B2', self.parametros[0][0],decimales)
            worksheet.write_row('B3', self.parametros[0][1],decimales)
            worksheet.write_row('B4', self.parametros[0][2],decimales)
            worksheet.write_row('B5', self.parametros[0][3],decimales)
            worksheet.write_row('B6', self.parametros[0][4],decimales)
            worksheet.write_row('B7', self.parametros[0][5],decimales)
            worksheet.write_row('B8', self.parametros[0][6],decimales)
            worksheet.write_row('B9', self.parametros[0][7],decimales)

            worksheet.write_row('N1', funciones.bandas_tercios,bordeynegrita)
            worksheet.write_column('M2', ["EDT(s)", "T20(s)", "T30(s)", "IACC early", "C50(dB)", "C80(dB)", "Tt(ms)",
                                          "EDTt(s)"],bordeynegrita)

            # Parametros Tercios L
            worksheet.write_row('N2', self.parametros[1][0],decimales)
            worksheet.write_row('N3', self.parametros[1][1],decimales)
            worksheet.write_row('N4', self.parametros[1][2],decimales)
            worksheet.write_row('N5', self.parametros[1][3],decimales)
            worksheet.write_row('N6', self.parametros[1][4],decimales)
            worksheet.write_row('N7', self.parametros[1][5],decimales)
            worksheet.write_row('N8', self.parametros[1][6],decimales)
            worksheet.write_row('N9', self.parametros[1][7],decimales)

            if len(self.parametros) > 2: #Para audios estereo
                worksheet.write(0, 12, "Left",bordeynegrita)
                worksheet.write(0, 0, "Left",bordeynegrita)

                worksheet.write(10, 0, "Right",bordeynegrita)
                worksheet.write_row('B11', funciones.bandas_octavas,bordeynegrita)
                worksheet.write_column('A12',
                                       ["EDT(s)", "T20(s)", "T30(s)", "IACC early", "C50(dB)", "C80(dB)", "Tt(ms)",
                                        "EDTt(s)"],bordeynegrita)

                #Parametros Octavas R
                worksheet.write_row('B12', self.parametros[2][0],decimales)
                worksheet.write_row('B13', self.parametros[2][1],decimales)
                worksheet.write_row('B14', self.parametros[2][2],decimales)
                worksheet.write_row('B15', self.parametros[2][3],decimales)
                worksheet.write_row('B16', self.parametros[2][4],decimales)
                worksheet.write_row('B17', self.parametros[2][5],decimales)
                worksheet.write_row('B18', self.parametros[2][6],decimales)
                worksheet.write_row('B19', self.parametros[2][7],decimales)

                worksheet.write(10, 12, "Right",bordeynegrita)
                worksheet.write_row('N11', funciones.bandas_tercios,bordeynegrita)
                worksheet.write_column('M12',
                                       ["EDT(s)", "T20(s)", "T30(s)", "IACC early", "C50(dB)", "C80(dB)", "Tt(ms)",
                                        "EDTt(s)"],bordeynegrita)

                #Parametros Tercios R
                worksheet.write_row('N12', self.parametros[3][0],decimales)
                worksheet.write_row('N13', self.parametros[3][1],decimales)
                worksheet.write_row('N14', self.parametros[3][2],decimales)
                worksheet.write_row('N15', self.parametros[3][3],decimales)
                worksheet.write_row('N16', self.parametros[3][4],decimales)
                worksheet.write_row('N17', self.parametros[3][5],decimales)
                worksheet.write_row('N18', self.parametros[3][6],decimales)
                worksheet.write_row('N19', self.parametros[3][7],decimales)

            workbook.close()
        dialog.Destroy()

    # Función para exportar los datos a CSV
    def exportarCSV(self, e):
        wildcard = "csv (*.csv)|*.csv"

        dialog = wx.FileDialog(
            self, message="Guardar archivo",
            defaultDir=self.currentDirectory,
            defaultFile="Datos Medición",
            wildcard=wildcard,
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dialog.ShowModal() == wx.ID_OK:
            paths = dialog.GetPath()

            with open(paths, mode='w', newline='') as parametros_senial:

                data = csv.writer(parametros_senial, delimiter=',')
                parametros = ["EDT(s)", "T20(s)", "T30(s)", "IACC early", "C50(dB)", "C80(dB)", "Tt(ms)",
                              "EDTt(s)"]

                for i in range(len(self.parametros)):
                    if i == 0 and len(self.parametros) == 2:
                        data.writerow(["Octavas"])
                        data.writerow(funciones.bandas_octavas)
                    elif i == 0 and len(self.parametros) == 4:
                        data.writerow(["Octavas L"])
                        data.writerow(funciones.bandas_octavas)
                    if i == 1 and len(self.parametros) == 2:
                        data.writerow(["Tercios de octava"])
                        data.writerow(funciones.bandas_tercios)
                    elif i == 1 and len(self.parametros) == 4:
                        data.writerow(["Tercios de octava L"])
                        data.writerow(funciones.bandas_tercios)
                    if i == 2:
                        data.writerow(["Octavas R"])
                        data.writerow(funciones.bandas_octavas)
                    if i == 3:
                        data.writerow(["Tercios de octava R"])
                        data.writerow(funciones.bandas_tercios)

                    for j in range(len(self.parametros[0])):
                        datos_parametro = [parametros[j]]
                        for k in range(len(self.parametros[0][0])):
                            dato = self.parametros[i][j][k]
                            datos_parametro.append(dato)
                        data.writerow(datos_parametro)
                    data.writerow('\n')

        dialog.Destroy()

    #Función para cerrar GUI
    def salir(self, event):
        self.Close()


    #Función para habilitar el tamaño de ventana de la MMF
    def habilitar(self,event):

        opcion=self.m_choice3.GetSelection()

        if opcion==0:   #Si se elige Schoreder se deshabilita
            self.m_textCtrl7.Enable(False)

        if opcion==1:   #Si se elige MMF se habilita
            self.m_textCtrl7.Enable(True)


    #Función para calcular los parametros y mostrarlos en la GUI
    def calcularParametros(self, event):

        self.bandas=[]
        self.dbfs = []
        self.td = []
        self.integral=[]
        self.parametros=[]

        #Si la señal es estereo se muestran los resultados de ambos canales
        if (len(self.senial_promedio)==2 and self.m_notebook1.GetPageCount()==2):

            self.m_notebook1.AddPage(self.m_panel71, u"Octavas-R", False)
            self.m_notebook1.AddPage(self.m_panel61, u"Tercios de Octava-R", False)
            self.m_notebook1.SetPageText(0,u"Octavas-L")
            self.m_notebook1.SetPageText(1, u"Tercios de Octava-L")


        else:
            if(self.m_notebook1.GetPageCount()==4 and len(self.senial_promedio)==1):

                self.m_notebook1.SetPageText(0, u"Octavas")
                self.m_notebook1.SetPageText(1, u"Tercios de Octava")
                self.m_notebook1.RemovePage(2)
                self.m_notebook1.RemovePage(2)


        for i,canal in enumerate(self.senial_promedio): #Calculo para cada canal
            #OCTAVAS
            bandas = funciones.filtrado(canal, self.fs, 1, 2)#Filtrado de la señal
            self.bandas.append(bandas)
            dbfs = funciones.energy(bandas) #Paso a energía
            self.dbfs.append(dbfs)
            td = funciones.lundeby(dbfs,self.fs)#Función de Lundeby
            self.td.append(td)
            if self.m_choice3.GetSelection()==0: #Calculo de Schoreder

                integral = funciones.schoeder(bandas, td)

            else: #Calculo de MMF
                ventana_tiempo=int(self.m_textCtrl7.GetValue())
                ventana_muestras=int(ventana_tiempo*self.fs/1000)#Ventana elegida por el usuario en muestras

                integral=funciones.mediana_movil(dbfs,td,ventana_muestras)


            self.integral.append(integral)
            c50,c80 = funciones.claridad(bandas, self.fs,td) #Calculo de c50, c80
            EDT, T20, T30 = funciones.parametros(integral, self.fs) #Calculo de EDT, T20, T30
            Tt =funciones.transitiontime(bandas,self.fs) #Calculo de Tt
            EDTt = funciones.earlyDecayTT(integral,Tt,self.fs) #Calculo de EDTt

            parametros=[EDT,T20,T30,[], c50, c80,Tt, EDTt]
            self.parametros.append(parametros)

            for fila, parametro in enumerate(parametros): #Se muestras los resultados en grilla
                for columna, banda in enumerate(parametro):
                    if(i==0):
                        self.m_grid2.SetCellValue(fila, columna, "{:.3f}".format(parametros[fila][columna]))
                    else:
                        self.m_grid4.SetCellValue(fila, columna, "{:.3f}".format(parametros[fila][columna]))


            #TERCIOS: Se siguen los mismos pasos que en octavas

            rir_invertida = np.flip(canal) #Se invierte la RIR
            bandas_invertidas = funciones.filtrado(rir_invertida, self.fs, 3, 2) #Se filtra
            bandas = np.flip(bandas_invertidas, axis=1)#Se invierten las bandas filtradas nuevamente
            self.bandas.append(bandas)
            dbfs = funciones.energy(bandas)
            self.dbfs.append(dbfs)
            td = funciones.lundeby(dbfs,self.fs)
            self.td.append(td)
            if self.m_choice3.GetSelection() == 0:

                integral = funciones.schoeder(bandas, td)

            else:
                ventana_tiempo = int(self.m_textCtrl7.GetValue())
                ventana_muestras = int(ventana_tiempo * self.fs / 1000)

                integral = funciones.mediana_movil(dbfs, td, ventana_muestras)

            self.integral.append(integral)
            c50, c80 = funciones.claridad(bandas, self.fs, td)
            EDT, T20, T30 = funciones.parametros(integral, self.fs)
            Tt = funciones.transitiontime(bandas, self.fs)
            EDTt = funciones.earlyDecayTT(integral, Tt, self.fs)

            parametros = [EDT,T20, T30,[], c50, c80, Tt,EDTt]
            self.parametros.append(parametros)

            for fila, parametro in enumerate(parametros):
                for columna, banda in enumerate(parametro):
                    if (i == 0):
                        self.m_grid1.SetCellValue(fila, columna, "{:.3f}".format(parametros[fila][columna]))
                    else:
                        self.m_grid3.SetCellValue(fila, columna, "{:.3f}".format(parametros[fila][columna]))

        #Si el audio es estereo se calcula el IACC y se muestra
        if len(self.senial_promedio) == 2:
            iacc_octavas=funciones.IACC(self.bandas[0], self.bandas[2], self.fs) #IACC Octavas
            self.parametros[0][3] = iacc_octavas
            self.parametros[2][3] = iacc_octavas
            iacc_tercios=funciones.IACC(self.bandas[1], self.bandas[3], self.fs)#IACC Tercios
            self.parametros[1][3] = iacc_tercios
            self.parametros[3][3] = iacc_tercios

            for i in range(len(iacc_octavas)):
                self.m_grid2.SetCellValue(3, i, "{:.3f}".format(iacc_octavas[i]))
                self.m_grid4.SetCellValue(3, i, "{:.3f}".format(iacc_octavas[i]))
            for i in range(len(iacc_tercios)):
                self.m_grid1.SetCellValue(3, i, "{:.3f}".format(iacc_tercios[i]))
                self.m_grid3.SetCellValue(3, i, "{:.3f}".format(iacc_tercios[i]))
        else:
            self.parametros[0][3] = ["-"] * 10
            self.parametros[1][3] = ["-"] * 30
            for i in range(10):
                self.m_grid2.SetCellValue(3, i, "-")
            for i in range(30):
                self.m_grid1.SetCellValue(3, i, "-")


    #Función para abrir la ventana de configuración de filtro inverso
    def abrirConfSine(self,event):
        config_sine=MyFrame21(self)
        config_sine.Show()


    #Función para gráficar la energía de la señal y el suavizado al seleccionar una columna de la grilla
    def graficar(self,event):
        panel=self.m_notebook1.GetSelection()

        banda=[]
        if panel==0:
            banda=self.m_grid2.GetSelectedCols()
        if panel == 1:
            banda = self.m_grid1.GetSelectedCols()
        if panel == 2:
            banda = self.m_grid4.GetSelectedCols()
        if panel == 3:
            banda = self.m_grid3.GetSelectedCols()

        senal=self.dbfs[panel][banda[0]]
        sch=self.integral[panel][banda[0]]
        W,H=self.m_panel9.GetSize()

        grafico=funciones.ploteo_banda(senal,sch,self.fs,W,H)


        self.canvas.Destroy()
        self.canvas = FigureCanvas(self.m_panel9, -1, grafico)
        plt.close(grafico)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 0)
        self.m_panel9.SetSizerAndFit(sizer)
        self.canvas.draw()


#Ventana de parametros de filtro inverso
class MyFrame21(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Filtro-Inverso", pos=wx.DefaultPosition,
                          size=wx.Size(342, 290),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.Size(342, 290), wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        self.parent=parent
        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)
        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText9 = wx.StaticText(self, wx.ID_ANY, u"Canales", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText9.Wrap(-1)
        bSizer4.Add(self.m_staticText9, 2, wx.ALL, 5)

        self.m_radioBtn1 = wx.RadioButton(self, wx.ID_ANY, u"Mono", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        self.m_radioBtn1.SetValue(True)
        bSizer4.Add(self.m_radioBtn1, 1, wx.ALL, 5)

        self.m_radioBtn2 = wx.RadioButton(self, wx.ID_ANY, u"Estereo", wx.DefaultPosition,
                                          wx.DefaultSize, 0)
        bSizer4.Add(self.m_radioBtn2, 1, wx.ALL, 5)
        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"Tipo de Sine", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer6.Add(self.m_staticText1, 1, wx.ALL, 5)

        m_choice1Choices = [u"Logarítimico", u"Lineal"]
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(0)
        bSizer6.Add(self.m_choice1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer6, 1, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"Frecuencia Inicial(Hz)", wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer7.Add(self.m_staticText2, 1, wx.ALL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer7.Add(self.m_textCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer7, 1, wx.EXPAND, 5)

        bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText3 = wx.StaticText(self, wx.ID_ANY, u"Frecuencia final(Hz)", wx.DefaultPosition, wx.DefaultSize,
                                           0)
        self.m_staticText3.Wrap(-1)
        bSizer8.Add(self.m_staticText3, 1, wx.ALL, 5)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, u"20000", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer8.Add(self.m_textCtrl2, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer8, 1, wx.EXPAND, 5)

        bSizer9 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText4 = wx.StaticText(self, wx.ID_ANY, u"Duración(s)", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText4.Wrap(-1)
        bSizer9.Add(self.m_staticText4, 1, wx.ALL, 5)

        self.m_textCtrl3 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer9.Add(self.m_textCtrl3, 1, wx.ALL | wx.EXPAND, 5)

        bSizer1.Add(bSizer9, 1, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText5 = wx.StaticText(self, wx.ID_ANY, u"Frecuencia de muestreo", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText5.Wrap(-1)
        bSizer10.Add(self.m_staticText5, 1, wx.ALL, 5)

        self.m_textCtrl4 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer10.Add(self.m_textCtrl4, 1, wx.ALL | wx.EXPAND, 5)
        bSizer1.Add(bSizer10, 1, wx.EXPAND, 5)
        self.m_button2 = wx.Button(self, wx.ID_ANY, u"Aplicar filtro inverso", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.m_button2, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)
        # Connect Events
        self.m_button2.Bind(wx.EVT_BUTTON, self.generarFiltro)

    def __del__(self):
        pass

    # Funcion para generar filtro y obtener RIR
    def generarFiltro(self, event):

        parametros_filtro=[]

        try:
            mono = self.m_radioBtn1.GetValue()

            if (mono):
                canales = 1
            else:
                canales = 2

            tipo_sine = self.m_choice1.GetSelection()

            f_inicio=int(self.m_textCtrl1.GetValue())

            f_fin=int(self.m_textCtrl2.GetValue())

            duracion = int(self.m_textCtrl3.GetValue())

            frecuencia_muestreo= int(self.m_textCtrl4.GetValue())

            tamanio_ventana = int((1 / f_inicio) * 1000)

            self.parent.m_textCtrl7.SetValue(str(tamanio_ventana))

            parametros_filtro = [canales, tipo_sine, f_inicio, f_fin, duracion, frecuencia_muestreo]

            filtro_inverso=funciones.generar_filtro(parametros_filtro) #Se genera filtro

            sine_grabado = [self.parent.m_dataViewListCtrl1.GetValue(i, 0) for i in range(self.parent.m_dataViewListCtrl1.GetItemCount())]
            fs, sine_grabado = funciones.promediado_seniales(sine_grabado[0]) #Se extrae data de sine grabado
            rir=funciones.rir(sine_grabado,filtro_inverso) #Se obtiene respuesta al impulso
            self.parent.senial_promedio=rir

            self.Destroy()

        except:
            wx.MessageDialog(
                None,
                ('Datos erroneos o faltantes'),
                ('Error!'),
                wx.OK
            ).ShowModal()

        return parametros_filtro