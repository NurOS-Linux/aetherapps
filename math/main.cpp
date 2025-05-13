// main.cpp
#include <QApplication>
#include <QMainWindow>
#include <QGridLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QVBoxLayout>
#include <QWidget>
#include <QFont>
#include <QString>
#include <QLabel>
#include <QGraphicsDropShadowEffect>
#include <QPropertyAnimation>
#include <QStack>
#include <QRegularExpression>
#include <cmath>

class Calculator : public QMainWindow {
private:
    QLineEdit* display;
    QLineEdit* historyDisplay;
    QString currentInput;
    QString storedNumber;
    char pendingOperation;
    bool waitingForOperand;
    QStack<double> memoryStack;
    
public:
    Calculator(QWidget* parent = nullptr) : QMainWindow(parent) {
        setWindowTitle("AMath (AetherDE Math)");
        setFixedSize(360, 540);
        
        // Установка темной темы со скругленными квадратами и большими отступами
        setStyleSheet(
            "QMainWindow { background-color: #121212; }"
            "QWidget { background-color: #121212; color: #FFFFFF; }"
            "QLineEdit { background-color: #1E1E1E; color: #FFFFFF; border: none; border-radius: 12px; padding: 15px; font-size: 28px; margin: 5px; }"
            "QLineEdit#historyDisplay { background-color: transparent; color: #777777; border: none; padding: 5px 15px; font-size: 14px; }"
            "QPushButton { background-color: #1E1E1E; color: #FFFFFF; border: none; border-radius: 12px; padding: 15px; font-size: 16px; margin: 5px; }"
            "QPushButton:hover { background-color: #2A2A2A; }"
            "QPushButton:pressed { background-color: #383838; transform: scale(0.95); }"
            "QPushButton#equalButton { background-color: #424242; color: #FFFFFF; }"
            "QPushButton#equalButton:hover { background-color: #4F4F4F; }"
            "QPushButton#operationButton { background-color: #212121; color: #BBBBBB; }"
            "QPushButton#operationButton:hover { background-color: #2C2C2C; }"
            "QPushButton#specialButton { background-color: #1A1A1A; color: #5D87FF; }"
            "QPushButton#specialButton:hover { background-color: #252525; }"
            "QLabel { color: #888888; font-size: 12px; }"
        );
        
        QWidget* centralWidget = new QWidget(this);
        setCentralWidget(centralWidget);
        
        QVBoxLayout* mainLayout = new QVBoxLayout(centralWidget);
        mainLayout->setSpacing(12);  // Увеличенный отступ между элементами
        mainLayout->setContentsMargins(15, 15, 15, 15);
        
        // Заголовок
        QLabel* titleLabel = new QLabel("AMath", this);
        titleLabel->setAlignment(Qt::AlignLeft);
        titleLabel->setStyleSheet("font-size: 16px; color: #888888; margin-bottom: 5px;");
        mainLayout->addWidget(titleLabel);
        
        // История вычислений
        historyDisplay = new QLineEdit("");
        historyDisplay->setObjectName("historyDisplay");
        historyDisplay->setReadOnly(true);
        historyDisplay->setAlignment(Qt::AlignRight);
        historyDisplay->setFixedHeight(30);
        mainLayout->addWidget(historyDisplay);
        
        // Дисплей
        display = new QLineEdit("0");
        display->setReadOnly(true);
        display->setAlignment(Qt::AlignRight);
        display->setFixedHeight(80);
        
        // Добавление тени для дисплея
        QGraphicsDropShadowEffect* shadowEffect = new QGraphicsDropShadowEffect(this);
        shadowEffect->setBlurRadius(15);
        shadowEffect->setColor(QColor(0, 0, 0, 80));
        shadowEffect->setOffset(0, 2);
        display->setGraphicsEffect(shadowEffect);
        
        mainLayout->addWidget(display);
        
        // Сетка кнопок
        QGridLayout* buttonsLayout = new QGridLayout();
        buttonsLayout->setSpacing(10);  // Увеличенный отступ между кнопками
        
        // Функциональные кнопки
        QPushButton* clearButton = createButton("C");
        QPushButton* clearEntryButton = createButton("CE");
        QPushButton* backspaceButton = createButton("⌫");
        QPushButton* percentButton = createButton("%");
        
        // Числовые кнопки
        QPushButton* digitButtons[10];
        for (int i = 0; i < 10; ++i) {
            digitButtons[i] = createButton(QString::number(i));
        }
        
        // Операционные кнопки
        QPushButton* divideButton = createButton("÷");
        divideButton->setObjectName("operationButton");
        QPushButton* multiplyButton = createButton("×");
        multiplyButton->setObjectName("operationButton");
        QPushButton* subtractButton = createButton("-");
        subtractButton->setObjectName("operationButton");
        QPushButton* addButton = createButton("+");
        addButton->setObjectName("operationButton");
        QPushButton* equalButton = createButton("=");
        equalButton->setObjectName("equalButton");
        QPushButton* decimalButton = createButton(".");
        QPushButton* negateButton = createButton("±");
        
        // Новые специальные функции
        QPushButton* sqrtButton = createButton("√x");
        sqrtButton->setObjectName("specialButton");
        QPushButton* powerButton = createButton("x²");
        powerButton->setObjectName("specialButton");
        QPushButton* inverseButton = createButton("1/x");
        inverseButton->setObjectName("specialButton");
        QPushButton* memoryPushButton = createButton("M+");
        memoryPushButton->setObjectName("specialButton");
        QPushButton* memoryPopButton = createButton("M-");
        memoryPopButton->setObjectName("specialButton");
        QPushButton* sinButton = createButton("sin");
        sinButton->setObjectName("specialButton");
        QPushButton* cosButton = createButton("cos");
        cosButton->setObjectName("specialButton");
        
        // Первый ряд
        buttonsLayout->addWidget(clearButton, 0, 0);
        buttonsLayout->addWidget(clearEntryButton, 0, 1);
        buttonsLayout->addWidget(backspaceButton, 0, 2);
        buttonsLayout->addWidget(divideButton, 0, 3);
        
        // Второй ряд
        buttonsLayout->addWidget(digitButtons[7], 1, 0);
        buttonsLayout->addWidget(digitButtons[8], 1, 1);
        buttonsLayout->addWidget(digitButtons[9], 1, 2);
        buttonsLayout->addWidget(multiplyButton, 1, 3);
        
        // Третий ряд
        buttonsLayout->addWidget(digitButtons[4], 2, 0);
        buttonsLayout->addWidget(digitButtons[5], 2, 1);
        buttonsLayout->addWidget(digitButtons[6], 2, 2);
        buttonsLayout->addWidget(subtractButton, 2, 3);
        
        // Четвертый ряд
        buttonsLayout->addWidget(digitButtons[1], 3, 0);
        buttonsLayout->addWidget(digitButtons[2], 3, 1);
        buttonsLayout->addWidget(digitButtons[3], 3, 2);
        buttonsLayout->addWidget(addButton, 3, 3);
        
        // Пятый ряд
        buttonsLayout->addWidget(negateButton, 4, 0);
        buttonsLayout->addWidget(digitButtons[0], 4, 1);
        buttonsLayout->addWidget(decimalButton, 4, 2);
        buttonsLayout->addWidget(equalButton, 4, 3);
        
        // Шестой ряд - специальные функции
        buttonsLayout->addWidget(percentButton, 5, 0);
        buttonsLayout->addWidget(sqrtButton, 5, 1);
        buttonsLayout->addWidget(powerButton, 5, 2);
        buttonsLayout->addWidget(inverseButton, 5, 3);
        
        // Седьмой ряд - дополнительные функции
        buttonsLayout->addWidget(memoryPushButton, 6, 0);
        buttonsLayout->addWidget(memoryPopButton, 6, 1);
        buttonsLayout->addWidget(sinButton, 6, 2);
        buttonsLayout->addWidget(cosButton, 6, 3);
        
        mainLayout->addLayout(buttonsLayout);
        
        // Подвал с обновленной версией 1.3.2
        QLabel* footerLabel = new QLabel("AetherDE Math v1.3.2", this);
        footerLabel->setAlignment(Qt::AlignRight);
        footerLabel->setStyleSheet("font-size: 10px; color: #444444; margin-top: 5px;");
        mainLayout->addWidget(footerLabel);
        
        // Инициализация переменных
        currentInput = "";
        storedNumber = "";
        pendingOperation = 0;
        waitingForOperand = true;
        
        // Подключение сигналов
        for (int i = 0; i < 10; ++i) {
            connect(digitButtons[i], &QPushButton::clicked, this, [this, i]() {
                digitClicked(QString::number(i));
                animateButton(qobject_cast<QPushButton*>(sender()));
            });
        }
        
        connect(decimalButton, &QPushButton::clicked, this, [this]() {
            if (waitingForOperand || currentInput.isEmpty()) {
                currentInput = "0";
                waitingForOperand = false;
            }
            
            if (!currentInput.contains('.'))
                currentInput += '.';
                
            display->setText(currentInput);
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(clearButton, &QPushButton::clicked, this, [this]() {
            currentInput = "";
            storedNumber = "";
            pendingOperation = 0;
            waitingForOperand = true;
            display->setText("0");
            historyDisplay->setText("");
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(clearEntryButton, &QPushButton::clicked, this, [this]() {
            currentInput = "";
            waitingForOperand = true;
            display->setText("0");
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(backspaceButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty() && !waitingForOperand) {
                currentInput.chop(1);
                if (currentInput.isEmpty()) {
                    currentInput = "";
                    waitingForOperand = true;
                    display->setText("0");
                } else {
                    display->setText(currentInput);
                }
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(negateButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty() && currentInput != "0") {
                if (currentInput.startsWith('-')) {
                    currentInput.remove(0, 1);
                } else {
                    currentInput = '-' + currentInput;
                }
                display->setText(currentInput);
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(percentButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                double value = currentInput.toDouble() / 100.0;
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(sqrtButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                double value = currentInput.toDouble();
                if (value >= 0) {
                    historyDisplay->setText("√(" + currentInput + ")");
                    value = sqrt(value);
                    currentInput = QString::number(value, 'g', 12);
                    display->setText(currentInput);
                    waitingForOperand = true;
                }
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        // Новые функции
        connect(powerButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                double value = currentInput.toDouble();
                historyDisplay->setText("(" + currentInput + ")²");
                value = value * value;
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(inverseButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty() && currentInput.toDouble() != 0) {
                double value = 1.0 / currentInput.toDouble();
                historyDisplay->setText("1/(" + currentInput + ")");
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(memoryPushButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                memoryStack.push(currentInput.toDouble());
                historyDisplay->setText("M+ (" + currentInput + ")");
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(memoryPopButton, &QPushButton::clicked, this, [this]() {
            if (!memoryStack.isEmpty()) {
                double value = memoryStack.pop();
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                historyDisplay->setText("M- → " + currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(sinButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                double value = sin(currentInput.toDouble() * M_PI / 180.0); // В градусах
                historyDisplay->setText("sin(" + currentInput + "°)");
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(cosButton, &QPushButton::clicked, this, [this]() {
            if (!currentInput.isEmpty()) {
                double value = cos(currentInput.toDouble() * M_PI / 180.0); // В градусах
                historyDisplay->setText("cos(" + currentInput + "°)");
                currentInput = QString::number(value, 'g', 12);
                display->setText(currentInput);
                waitingForOperand = true;
            }
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        // Подключение операций
        connect(addButton, &QPushButton::clicked, this, [this]() {
            operatorClicked('+');
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(subtractButton, &QPushButton::clicked, this, [this]() {
            operatorClicked('-');
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(multiplyButton, &QPushButton::clicked, this, [this]() {
            operatorClicked('*');
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(divideButton, &QPushButton::clicked, this, [this]() {
            operatorClicked('/');
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
        
        connect(equalButton, &QPushButton::clicked, this, [this]() {
            equalClicked();
            animateButton(qobject_cast<QPushButton*>(sender()));
        });
    }
    
private:
    QPushButton* createButton(const QString& text) {
        QPushButton* button = new QPushButton(text);
        button->setFixedSize(70, 54);  // Немного уменьшенный размер для квадратных кнопок
        button->setCursor(Qt::PointingHandCursor);
        return button;
    }
    
    void animateButton(QPushButton* button) {
        if (!button) return;
        
        QPropertyAnimation* animation = new QPropertyAnimation(button, "geometry");
        animation->setDuration(100);
        QRect startGeometry = button->geometry();
        QRect endGeometry = startGeometry;
        
        // Немного уменьшаем кнопку и возвращаем к исходному размеру
        animation->setStartValue(startGeometry);
        endGeometry.adjust(2, 2, -2, -2);
        animation->setKeyValueAt(0.5, endGeometry);
        animation->setEndValue(startGeometry);
        animation->start(QAbstractAnimation::DeleteWhenStopped);
    }
    
    void digitClicked(const QString& digit) {
        if (waitingForOperand) {
            currentInput = digit;
            waitingForOperand = false;
        } else {
            if (currentInput == "0")
                currentInput = digit;
            else
                currentInput += digit;
        }
        
        display->setText(currentInput);
    }
    
    void operatorClicked(char op) {
        if (!currentInput.isEmpty()) {
            if (!storedNumber.isEmpty() && !waitingForOperand) {
                equalClicked();
            }
            
            storedNumber = currentInput;
            pendingOperation = op;
            waitingForOperand = true;
            
            // Обновление истории
            QString opSymbol;
            switch (op) {
                case '+': opSymbol = " + "; break;
                case '-': opSymbol = " - "; break;
                case '*': opSymbol = " × "; break;
                case '/': opSymbol = " ÷ "; break;
            }
            historyDisplay->setText(storedNumber + opSymbol);
        } else if (!storedNumber.isEmpty()) {
            // Позволяет изменить операцию, если число уже введено
            pendingOperation = op;
            
            // Обновление символа операции в истории
            QString opSymbol;
            switch (op) {
                case '+': opSymbol = " + "; break;
                case '-': opSymbol = " - "; break;
                case '*': opSymbol = " × "; break;
                case '/': opSymbol = " ÷ "; break;
            }
            
            // Обновляем только символ операции
            QString history = historyDisplay->text();
            // Используем QRegularExpression вместо QRegExp
            QRegularExpression re("[ ][+\\-×÷][ ]");
            if (history.contains(re)) {
                history.replace(re.match(history).captured(), opSymbol);
                historyDisplay->setText(history);
            } else {
                historyDisplay->setText(storedNumber + opSymbol);
            }
        }
    }
    
    void equalClicked() {
        if (storedNumber.isEmpty() || pendingOperation == 0 || (waitingForOperand && currentInput.isEmpty()))
            return;
        
        if (waitingForOperand && !currentInput.isEmpty()) {
            // Если ожидается операнд, но ввод не пуст, используем его
            waitingForOperand = false;
        }
        
        double storedValue = storedNumber.toDouble();
        double current = waitingForOperand ? storedValue : currentInput.toDouble();
        double result = 0.0;
        
        switch (pendingOperation) {
            case '+':
                result = storedValue + current;
                break;
            case '-':
                result = storedValue - current;
                break;
            case '*':
                result = storedValue * current;
                break;
            case '/':
                if (current != 0.0)
                    result = storedValue / current;
                else {
                    display->setText("Error");
                    historyDisplay->setText("Division by zero");
                    currentInput = "";
                    storedNumber = "";
                    pendingOperation = 0;
                    waitingForOperand = true;
                    return;
                }
                break;
        }
        
        // Обновление истории
        historyDisplay->setText(historyDisplay->text() + (waitingForOperand ? "" : currentInput) + " = ");
        
        currentInput = QString::number(result, 'g', 12);
        display->setText(currentInput);
        storedNumber = "";
        pendingOperation = 0;
        waitingForOperand = true;
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);
    
    Calculator calculator;
    calculator.show();
    
    return app.exec();
}