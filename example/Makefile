##
## Makefile for test in /home/antoine.stempfer/Projects/UnitTest
##
## Made by Bassintag
## Login   <bassintag@epitech.eu>
##
## Started on  Sat Nov 19 19:00:33 2016 Bassintag
## Last update Sun Nov 20 14:02:29 2016 Antoine Stempfer
##

CC	=	gcc

RM	=	rm -f

CFLAGS	=	-Wextra -Wall -Werror -I $(INC)

LDFLAGS	=

INC	=	include

NAME	=	test

OBJS	=	$(SRCS:.c=.o)

SRCS	=	example.c

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(OBJS) -o $(NAME) $(LDFLAGS)

clean:
	$(RM) $(OBJS)

fclean: clean
	$(RM) $(NAME)

re: clean all

.PHONY: all clean fclean re
