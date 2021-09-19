import threading
import decimal
n = decimal.Decimal('768768768')
print('{0:,}'.format(n).replace(',', ' '))




import PySimpleGUI as sg
layout = []
layout_line = [sg.Text("Your Gold:  "), sg.Text(size=(20,1), key='gold',visible=True), sg.Button('Refresh',key='refresh+gold', disabled=True)]
layout.append(layout_line)

layout_line = [sg.Text("                               STATS:           ")]
layout.append(layout_line)
layout_line = [sg.Text("Successful free accs raids: "), sg.Text(size=(10,1), key='raids',visible=True)]
layout.append(layout_line)

layout_line = [sg.Text("Cards dropped:"), sg.Text(size=(10,1), key='cards',visible=True)]
layout.append(layout_line)
# Create the window
window = sg.Window('Window Title', layout)


while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    print(event)
    if event == 'RunAll':
        pass
        # threading.Thread(target=runAll).start()


    if 'run_' in event:
        acc = event.split('_')[1]




# Finish up by removing from the screen
window.close()