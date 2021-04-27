import cv2


def detect_faces(reduced_image):
    face_cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(face_cascade)

    rectangles = face_classifier.detectMultiScale(
        reduced_image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30)
    )

    face_images = []

    for (x, y, w, h) in rectangles:
        ROI = reduced_image[y : y + h, x : x + w]
        face_images.append(ROI)

    return (rectangles, face_images)


def detect_faces_(image):
    face_cascade = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    face_classifier = cv2.CascadeClassifier(face_cascade)
    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_classifier.detectMultiScale(
        grey_image, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30)
    )

    face_images = []
    for (x, y, w, h) in faces:
        ROI = image[y : y + h, x : x + w]
        face_images.append(ROI)

    return (faces, face_images)


def show_webcam(mirror=False):
    video = cv2.VideoCapture(0)
    while True:
        check, frame = video.read()
        if mirror:
            frame = cv2.flip(frame, 1)

        data_faces, face_images = detect_faces(frame)
        modified_frame = add_rectangle(frame, data_faces)

        cv2.imshow("mywebcam", modified_frame)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()


def add_rectangle(frame, faces):
    color = (0, 255, 255)
    thickness = 15

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)

    return frame


def show_detected_faces(image, faces):
    print("Found {0} faces".format(len(faces)))
    color = (0, 0, 0)  # Black
    grosor = 2
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), color, grosor)

    cv2.imshow("found faces", image)
    cv2.waitKey(0)
