В методе `get_tfs_for_file` подсчитываются TF для каждого токена/лемммы в файле. Зависит от параметра `lemmatize`<br><br>
В методе `get_idfs` подсчитываются IDF для всех токенов/лемм. Зависит от параметра `lemmatize`<br><br>
Далее в методе `main` проходимся по всем файлам циклом и считаем TF-IDF