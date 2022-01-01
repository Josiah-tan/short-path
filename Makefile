SRC_DIR := .
OBJ_DIR := include

CC := g++
EXE := output
SRC := $(wildcard $(SRC_DIR)/*.cpp)
OBJ := $(SRC:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

CPPFLAGS := -Iinclude -MMD -MP
CFLAGS   := -Wall -fsanitize=address -g
LDFLAGS  := -Llib -fsanitize=address
LDLIBS   := -lm

.PHONY: all clean

all: $(EXE)

# if anything in the object directory changes, then 
$(EXE): $(OBJ)
		$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

# how to make anything in the object directory
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp | $(OBJ_DIR)
		$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(OBJ_DIR):
	mkdir -p $@

clean:
		@$(RM) -rv $(OBJ_DIR) $(EXE)

-include $(OBJ:.o=.d)
