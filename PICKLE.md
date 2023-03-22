# MacOS Pickle error on MultiPorcessing
### Code for multiprocessing to work on Macos:
```python
if sys.platform == 'darwin':
 	mp.set_start_method('fork')
```

### Explanation:

On MacOS, the default method for process iit has been changed so `spawn` instead of the expected `fork`.