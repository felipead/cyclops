COMPILER = g++ -Wall -g -D DEBUG

OSX_INCLUDE_DIR = -I/usr/local/include
OSX_LIBRARIES_DIR = -L/usr/local/lib
LINUX_INCLUDE_DIR = -I/usr/include
LINUX_LIBRARIES_DIR = -L/usr/lib

LIBRARIES = -lopencv_core -lopencv_imgproc -lopencv_highgui

RM = /bin/rm -f

APPLICATION = answer-sheet-recognizer

######################################################################

MODULES = 

######################################################################

osx:
	@echo "Compiling $(APPLICATION)..."
	$(COMPILER) -std=gnu++11 -stdlib=libstdc++ $(OSX_INCLUDE_DIR) $(MODULES) Main.cpp -o $(APPLICATION) $< $(OSX_LIBRARIES_DIR) $(LIBRARIES)

linux:
	@echo "Compiling $(APPLICATION)..."
	$(COMPILER) $(LINUX_INCLUDE_DIR) $(MODULES) Main.cpp -o $(APPLICATION) $< $(LINUX_LIBRARIES_DIR) $(LIBRARIES)

$(APPLICATION): Main.cpp $(MODULES)

run: $(APPLICATION)
	@./$(APPLICATION)

######################################################################

# Modules

# Module.o: Module.cpp Module.hpp
# 	@$(COMPILER) -c Module.cpp

######################################################################

clean:
	@$(RM) *.o */*.o core temp.dat $(APPLICATION)
