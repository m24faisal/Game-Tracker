#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDialog>
#include <QListWidget>
#include <QVBoxLayout>
#include <QDialogButtonBox>
#include <QPushButton>
#include <QProcess>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // Add a QListWidget to the main window to display added processes
    processListWidget = new QListWidget(this);
    setCentralWidget(processListWidget); // Set the QListWidget as the central widget
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

    // Create a QListWidget to display the process names
    QListWidget *dialogProcessListWidget = new QListWidget(processDialog);
    dialogProcessListWidget->setSelectionMode(QAbstractItemView::SingleSelection);

    // Create a QDialogButtonBox to hold the "Add Process" button
    QDialogButtonBox *buttonBox = new QDialogButtonBox(Qt::Horizontal, processDialog);
    QPushButton *addProcessButton = new QPushButton("Add Process", processDialog);
    buttonBox->addButton(addProcessButton, QDialogButtonBox::ActionRole);

    // Create a layout for the dialog
    QVBoxLayout *layout = new QVBoxLayout(processDialog);
    layout->addWidget(dialogProcessListWidget);
    layout->addWidget(buttonBox);
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
    dialogProcessListWidget->addItems(processNames);
    // Connect the Add Process button to a lambda that adds the selected process to the main window
    connect(addProcessButton, &QPushButton::clicked, this, [=]() {
        QListWidgetItem *selectedItem = dialogProcessListWidget->currentItem();
        if (selectedItem) {
            QString selectedProcessName = selectedItem->text();
            processListWidget->addItem(selectedProcessName);
        }
        processDialog->accept(); // Close the dialog
    });


    // Show the dialog
    processDialog->exec();
}
