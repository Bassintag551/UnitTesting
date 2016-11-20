/*
** lul.c for lul in /home/bassintag/Projects/UnitTest
** 
** Made by Antoine Stempfer
** Login   <antoine.stempfer@epitech.net>
** 
** Started on  Sat Nov 19 19:31:06 2016 Antoine Stempfer
** Last update Sun Nov 20 00:57:07 2016 Antoine Stempfer
*/

#include <stdlib.h>
#include <stdio.h>

int	main(int argc, char **argv)
{
  int	i;
  int	j;

  if (argc > 3)
    return (84);
  i = atoi(argv[1]);
  j = atoi(argv[2]);
  printf("%d", i + j);
  return (0);
}
