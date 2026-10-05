CXX := g++
CXXFLAGS := -std=c++20 -Wall -Wextra -g

# Every .cxx file in this directory becomes an object file target
SRCS := $(wildcard *.cxx) $(wildcard *.C)
OBJS := $(SRCS:.cxx=.o)
OBJS := $(OBJS:.C=.o)

TARGET := knit_calculator.exe

# Default target: build the final executable
all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET)

# Pattern rule: how to build any .o from its matching .cxx
# The header dependency (Gauge.h, Shape.h, ...) means editing a header
# also triggers a rebuild of anything that includes it.
%.o: %.cxx
	$(CXX) $(CXXFLAGS) -c $< -o $@
	
%.o: %.C
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Rule to run the executable
run: $(TARGET)
	$(TARGET)

# Remove build artifacts (del for windows, -rm for linux)
clean:
	del $(OBJS) $(TARGET)

# Rebuild from scratch
rebuild: clean all

# Targets that aren't real files
.PHONY: all clean rebuild