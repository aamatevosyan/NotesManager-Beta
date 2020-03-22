from PyQt5 import QtWidgets, QtGui


def get_QTabBar_style(background='#00ff00'):
    styleStr = str('''
        QTabBar::tab:!selected {{
            background: {};
        }}
    '''.format(background))

    return styleStr


class TabBar(QtWidgets.QTabBar):
    def __init__(self, parent):
        QtWidgets.QTabBar.__init__(self, parent)
        self.setStyleSheet(get_QTabBar_style())
        self.__coloredTabs = {}

    def colorTab(self, index, color='#ff0000'):
        if not 0 <= index < self.count():
            return
        proxy = self.__coloredTabs.get(index)
        if not proxy:
            proxy = self.__coloredTabs[index] = QtWidgets.QTabBar()
        proxy.setStyleSheet(get_QTabBar_style(color))
        self.update()

    def uncolorTab(self, index):
        try:
            self.__coloredTabs.pop(index)
            self.update()
        except:
            return

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            self.style().drawControl(
                QtWidgets.QStyle.CE_TabBarTabShape, opt, painter,
                self.__coloredTabs.get(i, self))
            self.style().drawControl(
                QtWidgets.QStyle.CE_TabBarTabLabel, opt, painter, self)


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        QtWidgets.QTabWidget.__init__(self, parent)
        # self.setStyleSheet(get_QTabWidget_style())
        tabBar = TabBar(self)
        self.setTabBar(tabBar)
        self.colorTab = tabBar.colorTab
        self.uncolorTab = tabBar.uncolorTab
