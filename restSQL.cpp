#include "TRestSql.h"

#include <iostream>

int main() {
  TRestSQL *restSql = new TRestSQL();
  std::cout << "test variable: " << restSql->x << std::endl;
  return 0;
}