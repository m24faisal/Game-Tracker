#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QProcess>
#include <QMessageBox>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_actionAdd_Game_triggered()
{
    // What to do when add game is clicked
    QProcess process;
#ifdef Q_OS_WIN
    process.start("tasklist");
#else
    process.start("ps", QStringList() << "-e");
#endif
    if(!process.waitForFinished()) {
        QMessageBox::critical(this,"Error", "Failed to retrieve process list.");
    }

    QString processOutput = process.readAllStandardOutput();

    QMessageBox msgBox;
    msgBox.setWindowTitle("Active Processes");
    msgBox.setText(processOutput);
    msgBox.setStandardButtons(QMessageBox::Ok);
    msgBox.exec();
}


