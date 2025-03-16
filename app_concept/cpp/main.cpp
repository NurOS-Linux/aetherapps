#include <QApplication>
#include <QMainWindow>
#include <QWidget>
#include <QVBoxLayout>
#include <QPushButton>
#include <QLabel>
#include <QLineEdit>
#include <QFrame>

class NurOSDarkWindow : public QMainWindow {
public:
    explicit NurOSDarkWindow(QWidget *parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("NurOS Dark App");
        setMinimumSize(800, 600);
        
        QWidget *centralWidget = new QWidget;
        setCentralWidget(centralWidget);
        
        QVBoxLayout *layout = new QVBoxLayout(centralWidget);
        
        QFrame *card = new QFrame;
        card->setObjectName("card");
        QVBoxLayout *cardLayout = new QVBoxLayout(card);
        
        QLabel *title = new QLabel("Welcome to NurOS Dark");
        title->setObjectName("title");
        
        QLineEdit *inputField = new QLineEdit;
        inputField->setPlaceholderText("Enter something...");
        inputField->setObjectName("input");
        
        QPushButton *actionButton = new QPushButton("Perform Action");
        actionButton->setObjectName("actionButton");
        
        cardLayout->addWidget(title);
        cardLayout->addWidget(inputField);
        cardLayout->addWidget(actionButton);
        
        layout->addWidget(card, 0, Qt::AlignCenter);
        
        setStyleSheet(R"(
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            #card {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 20px;
                min-width: 400px;
                max-width: 400px;
            }
            
            #title {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            
            QLineEdit {
                background-color: #3d3d3d;
                border: none;
                border-radius: 5px;
                padding: 10px;
                color: #ffffff;
                font-size: 14px;
                margin: 10px 0;
            }
            
            QLineEdit:focus {
                background-color: #454545;
                border: 2px solid #5c90ff;
            }
            
            QPushButton#actionButton {
                background-color: #5c90ff;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            
            QPushButton#actionButton:hover {
                background-color: #4a7ae0;
            }
            
            QPushButton#actionButton:pressed {
                background-color: #3e68c7;
            }
        )");
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    app.setStyle("Fusion");
    QPalette darkPalette;
    darkPalette.setColor(QPalette::Window, QColor(26, 26, 26));
    darkPalette.setColor(QPalette::WindowText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Base, QColor(45, 45, 45));
    darkPalette.setColor(QPalette::AlternateBase, QColor(53, 53, 53));
    darkPalette.setColor(QPalette::ToolTipBase, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::ToolTipText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Text, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Button, QColor(53, 53, 53));
    darkPalette.setColor(QPalette::ButtonText, QColor(255, 255, 255));
    darkPalette.setColor(QPalette::Link, QColor(92, 144, 255));
    app.setPalette(darkPalette);
    
    NurOSDarkWindow window;
    window.show();
    
    return app.exec();
}