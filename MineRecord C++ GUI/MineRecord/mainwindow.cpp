#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDialog>
#include <QPlainTextEdit>
#include <QVBoxLayout>
#include <QProcess>
#include <QDebug>

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
    // Create a dialog to display the process list
    QDialog *processDialog = new QDialog(this);
    processDialog->setWindowTitle("Active Processes");
    processDialog->setFixedSize(400, 300);

    // Create a QPlainTextEdit to display the process names
    QPlainTextEdit *processTextEdit = new QPlainTextEdit(processDialog);
    processTextEdit->setReadOnly(true); // Make it read-only

    // Create a layout for the dialog
    QVBoxLayout *layout = new QVBoxLayout(processDialog);
    layout->addWidget(processTextEdit);
    processDialog->setLayout(layout);

    // Retrieve the list of active processes using 'tasklist'
    QProcess process;
    process.start("tasklist", QStringList() << "/NH" << "/FO" << "CSV");
    process.waitForFinished();

    // Get the output and parse it to extract process names
    QString output = process.readAllStandardOutput();
    QStringList processNames;

    // Split the output into lines
    QStringList lines = output.split("\n", Qt::SkipEmptyParts);
    for (const QString &line : lines) {
        // Split each line by commas and extract the first column (process name)
        QStringList parts = line.split(",");
        if (parts.size() >= 1) {
            QString processName = parts[0].trimmed();
            if (!processName.isEmpty()) {
                // Remove quotes around the process name (if any)
                processName.remove('"');
                processNames.append(processName);
            }
        }
    }

    // Display the process names in the QPlainTextEdit
    processTextEdit->setPlainText(processNames.join("\n"));

    // Show the dialog
    processDialog->exec();
}
