

from recognize import *
from connect import *
from Adafruit_IO import Client, Data, MQTTClient
from firebase import save_record
from device import readSerial




def connect():
    aio = Client(AIO_USERNAME, AIO_KEY)
    client = MQTTClient(AIO_USERNAME, AIO_KEY)
    client.on_connect = connected
    client.on_disconnect = disconnected
    client.on_message = message
    client.on_subscribe = subscribe

    client.connect()
    client.loop_background()

    print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
    facenet_model = load_model('model/facenet_keras.h5')
    lcd_scr_data = Data(value="Loaded successfully...")
    client.publish(fr_screen, value=lcd_scr_data.value)
    print("Loaded successfully...")
    lcd_scr_data = Data(value="Welcome")
    client.publish(fr_screen, value=lcd_scr_data.value)
    while True:
        readSerial()
        img_val = None
        touch_val = aio.receive(fr_button2)
        if int(touch_val.value) == 1:
            lcd_scr_data = Data(value="Capturing...")
            client.publish(fr_screen, value=lcd_scr_data.value)
            img_val = get_image_pil()
            lcd_scr_data = Data(value="Captured")
            client.publish(fr_screen, value=lcd_scr_data.value)

        if img_val:
            svm_model = load('svm_model.joblib')
            try:
                screen, name, prob = predict('opencv_frame_0.png', svm_model, facenet_model)
                lcd_scr_data = Data(value=screen)
                client.publish(fr_screen, value=lcd_scr_data.value)
                save_record(name)
                if name != "Stranger":
                    client.publish(fr_button, value=0)
            except:
                lcd_scr_data = Data(value="No face detected !")
                client.publish(fr_screen, value=lcd_scr_data.value)

        aio.create_data(fr_button2, Data(value=0))




def main():
    connect()


if __name__ == "__main__":
    main()
    # # In case you want to train the svm model again #
    # facenet_model = load_model('model/facenet_keras.h5')
    # svm_model = train_svm_model(facenet_model)
