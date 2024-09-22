from pynput import keyboard

def on_press(key):
    try:
        print('Alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('Special key {0} pressed'.format(key))

def on_release(key):
    print('Key {0} released'.format(key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()