/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtGui/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QAction *About;
    QAction *Github;
    QAction *Qt;
    QAction *Updates;
    QAction *actionAdd_Game;
    QAction *actionStart_Recording;
    QAction *Web;
    QAction *actionExit_Application;
    QAction *actionRecord_Settings;
    QWidget *centralwidget;
    QMenuBar *menuBar;
    QMenu *File;
    QMenu *Setting;
    QMenu *menuInfo;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(800, 600);
        MainWindow->setStyleSheet(QString::fromUtf8("QWidget {\n"
"  background-color: black;\n"
"}"));
        About = new QAction(MainWindow);
        About->setObjectName("About");
        About->setCheckable(false);
        QIcon icon(QIcon::fromTheme(QIcon::ThemeIcon::HelpAbout));
        About->setIcon(icon);
        Github = new QAction(MainWindow);
        Github->setObjectName("Github");
        Github->setIcon(icon);
        Qt = new QAction(MainWindow);
        Qt->setObjectName("Qt");
        Qt->setIcon(icon);
        Updates = new QAction(MainWindow);
        Updates->setObjectName("Updates");
        QIcon icon1(QIcon::fromTheme(QIcon::ThemeIcon::SystemReboot));
        Updates->setIcon(icon1);
        actionAdd_Game = new QAction(MainWindow);
        actionAdd_Game->setObjectName("actionAdd_Game");
        QIcon icon2(QIcon::fromTheme(QIcon::ThemeIcon::ListAdd));
        actionAdd_Game->setIcon(icon2);
        actionStart_Recording = new QAction(MainWindow);
        actionStart_Recording->setObjectName("actionStart_Recording");
        QIcon icon3(QIcon::fromTheme(QIcon::ThemeIcon::MediaRecord));
        actionStart_Recording->setIcon(icon3);
        Web = new QAction(MainWindow);
        Web->setObjectName("Web");
        QIcon icon4(QIcon::fromTheme(QIcon::ThemeIcon::NetworkOffline));
        Web->setIcon(icon4);
        actionExit_Application = new QAction(MainWindow);
        actionExit_Application->setObjectName("actionExit_Application");
        QIcon icon5(QIcon::fromTheme(QIcon::ThemeIcon::ApplicationExit));
        actionExit_Application->setIcon(icon5);
        actionRecord_Settings = new QAction(MainWindow);
        actionRecord_Settings->setObjectName("actionRecord_Settings");
        actionRecord_Settings->setIcon(icon);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        MainWindow->setCentralWidget(centralwidget);
        menuBar = new QMenuBar(MainWindow);
        menuBar->setObjectName("menuBar");
        menuBar->setGeometry(QRect(0, 0, 800, 22));
        menuBar->setStyleSheet(QString::fromUtf8("QMenuBar {\n"
"    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,\n"
"                                      stop:0 lightgray, stop:1 darkgray);\n"
"    spacing: 3px; /* spacing between menu bar items */\n"
"}\n"
"\n"
"QMenuBar::item {\n"
"    padding: 1px 4px;\n"
"    background: transparent;\n"
"    border-radius: 4px;\n"
"	color: red\n"
"}\n"
"\n"
"QMenuBar::item:selected { /* when selected using mouse or keyboard */\n"
"    background: #a8a8a8;\n"
"}\n"
"\n"
"QMenuBar::item:pressed {\n"
"    background: #888888;\n"
"}\n"
"QMenu::item:selected { /* When hovered or focused */\n"
"    background-color: #0078d7; /* Highlight color (blue) */\n"
"    color: white; /* Text color on hover */\n"
"}"));
        File = new QMenu(menuBar);
        File->setObjectName("File");
        Setting = new QMenu(menuBar);
        Setting->setObjectName("Setting");
        menuInfo = new QMenu(menuBar);
        menuInfo->setObjectName("menuInfo");
        MainWindow->setMenuBar(menuBar);

        menuBar->addAction(File->menuAction());
        menuBar->addAction(Setting->menuAction());
        menuBar->addAction(menuInfo->menuAction());
        File->addAction(actionAdd_Game);
        File->addAction(actionStart_Recording);
        File->addAction(actionExit_Application);
        Setting->addAction(actionRecord_Settings);
        menuInfo->addAction(About);
        menuInfo->addAction(Github);
        menuInfo->addAction(Qt);
        menuInfo->addAction(Updates);
        menuInfo->addAction(Web);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        About->setText(QCoreApplication::translate("MainWindow", "About", nullptr));
        Github->setText(QCoreApplication::translate("MainWindow", "Github", nullptr));
        Qt->setText(QCoreApplication::translate("MainWindow", "Qt", nullptr));
        Updates->setText(QCoreApplication::translate("MainWindow", "Check for Updates", nullptr));
        actionAdd_Game->setText(QCoreApplication::translate("MainWindow", "Add Game", nullptr));
        actionStart_Recording->setText(QCoreApplication::translate("MainWindow", "Start Recording", nullptr));
        Web->setText(QCoreApplication::translate("MainWindow", "Visit Main Website", nullptr));
        actionExit_Application->setText(QCoreApplication::translate("MainWindow", "Exit Application", nullptr));
        actionRecord_Settings->setText(QCoreApplication::translate("MainWindow", "Record Settings", nullptr));
        File->setTitle(QCoreApplication::translate("MainWindow", "File", nullptr));
        Setting->setTitle(QCoreApplication::translate("MainWindow", "Settings", nullptr));
        menuInfo->setTitle(QCoreApplication::translate("MainWindow", "Info", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
