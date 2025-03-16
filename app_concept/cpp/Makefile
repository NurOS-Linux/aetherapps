CXX = clang++
CXXFLAGS = -Wall -Wextra -std=c++17 -O3
QT_INCLUDES = $(shell pkg-config --cflags Qt6Core Qt6Gui Qt6Widgets)
QT_LIBS = $(shell pkg-config --libs Qt6Core Qt6Gui Qt6Widgets)

TARGET = app
SOURCES = main.cpp

$(TARGET): $(SOURCES)
	$(CXX) $(CXXFLAGS) $(QT_INCLUDES) -o $@ $^ $(QT_LIBS)

clean:
	rm -f $(TARGET)

.PHONY: clean