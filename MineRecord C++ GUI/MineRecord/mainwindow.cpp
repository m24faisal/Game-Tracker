#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QProcess>
#include <QListWidget>
#include <QDialog>
#include <QVBoxLayout>
#include <QMessageBox>
#include <QTextEdit>

// Define a nested class for the process list dialog
class ProcessListDialog : public QDialog
{
    Q_OBJECT

public:
    explicit ProcessListDialog(QWidget *parent = nullptr)
        : QDialog(parent), processList(new QListWidget(this)), selectedProcess("")
    {
        setWindowTitle("Active Processes");
        setModal(true);

        QVBoxLayout *layout = new QVBoxLayout(this);
        layout->addWidget(processList);
        setLayout(layout);

        // Retrieve and display active processes
        QProcess process;
#ifdef Q_OS_WIN
        process.start("tasklist");
#else
        process.start("ps", QStringList() << "-e" << "-o" << "comm=");
#endif

        if (process.waitForFinished()) {
            QString output = process.readAllStandardOutput();
            QStringList processes = output.split("\n", Qt::SkipEmptyParts);

            for (const QString &processName : processes) {
                processList->addItem(processName.trimmed());
            }
        } else {
            processList->addItem("Failed to retrieve process list.");
        }

        // Connect double-click signal
        connect(processList, &QListWidget::itemDoubleClicked, this, &ProcessListDialog::onItemDoubleClicked);
    }

    QString getSelectedProcess() const
    {
        return selectedProcess;
    }

private slots:
    void onItemDoubleClicked(QListWidgetItem *item)
    {
        selectedProcess = item->text();
        accept(); // Close the dialog
    }

private:
    QListWidget *processList;
    QString selectedProcess;
};

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

void MainWindow::addProcessToMainWindow(const QString &processName)
{
    // Add the selected process to a QListWidget in the main window
    // Assuming you have a QListWidget named "listWidget" in your UI
    if (ui->listWidget) {
        ui->listWidget->addItem(processName);
    } else {
        qDebug() << "Selected process:" << processName; // Fallback to debug output
    }
}
void MainWindow::on_actionAdd_Game_triggered()
{
    // What to do when add game is clicked
    ProcessListDialog dialog(this);
    if (dialog.exec() == QDialog::Accepted) {
        QString selectedProcess = dialog.getSelectedProcess();
        addProcessToMainWindow(selectedProcess);
    }
}




