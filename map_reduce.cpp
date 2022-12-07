#include <algorithm>
#include <iostream>
#include <iterator>
#include <numeric>
#include <ranges>

int main() {
  auto map_func = [](auto i) { return i * i; };
  auto predicate = [](auto i) { return 4 == i % 10; };

  auto n = 10;
  auto rng = std::views::iota(0, n) // generates input list
        | std::views::transform(map_func) // Apply map function
        | std::views::filter(predicate);  // Apply filter

  auto max_value = std::reduce(rng.begin(), rng.end(), 0,
        [](auto a, auto b) { return std::max(a, b); }); 
  // reduce output list to single value

  std::cout << max_value << std::endl;
}