# Wordle Solver

Find it difficult to solve [Wordle](https://www.powerlanguage.co.uk/wordle/)? Here are some tools that help you:

* Find all 5-letter possible words that follow a given pattern

  ```python
  from solver import words_like
  
  print(words_like("_IGHT"))
  print(words_like("C___S"))
  ```

  

* `possible_words` / `possible_words_simple`: Narrow down all possible words given your previous attempt results

  ```python
  from solver import possible_words, possible_words_simple
  
  # A simple way: provide all your previous attempts and results
  print(possible_words_simple(
      trials=["slate", "mealy"],
      colors=["BYGBY", "BGGYG"]
  ))
  
  # Alternatively, provide all yellows, greens and blacks (letter and position)
  print(possible_words(
      yellows=["L2", "E5"],
      greens=["A3", "E2", "Y5"],
      blacks=("S", "T", "M")
  ))
  ```



* `suggestion`: Suggest your next attempt given your previous attempt results

  ```python
  from solver import suggestion
  
  print(suggestion(
      yellows=["L2", "E5"],
      greens=["A3", "E2", "Y5"],
      blacks=("S", "T", "M")
  ))
  ```

  

* `solver`:  Solve Wordle games automatically

  ```python
  from solver import solver, test_solver_single, test_solver_all
  
  # input the result each time (e.g. 'YBGBY') and get suggestion
  solver()
  
  # show how to solve one word
  test_solver_single('leafy')
  
  # evaluate on all 2.5k Wordle words 
  test_solver_all()
  ```
