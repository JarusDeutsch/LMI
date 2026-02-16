import QtQuick 2.15

Item {
    id: root
    width: 400
    height: 400

    Rectangle {
        anchors.fill: parent
        color: "white"
    }

    property real vGap: 40

    property real squareSize: Math.min(width, height - vGap) / 2

    Rectangle {
        id: topLeft
        width: root.squareSize
        height: root.squareSize
        color: "#880000"
        x: 0
        y: 0

        Text {
            text: 'color: "#880000"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: topRight
        width: root.squareSize
        height: root.squareSize
        color: "#FF0000"
        x: root.width - root.squareSize
        y: 0

        Text {
            text: 'color: "#FF0000"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: bottomLeft
        width: root.squareSize
        height: root.squareSize
        color: "#00FF00"
        x: 0
        y: root.squareSize + root.vGap

        Text {
            text: 'color: "#00FF00"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: bottomRight
        width: root.squareSize
        height: root.squareSize
        color: "#008800"
        x: root.width - root.squareSize
        y: root.squareSize + root.vGap

        Text {
            text: 'color: "#008800"'
            color: "black"
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Rectangle {
        id: centerRect
        width: root.squareSize * 1.2
        height: root.squareSize * 1.2
        color: "royalblue"
        radius: 25
        antialiasing: true
        anchors.centerIn: parent
        transformOrigin: Item.Center
        rotation: -45

        Text {
            anchors.centerIn: parent
            color: "white"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: 'color: "royalblue"\nradius: 25\nrotation: -45'
        }
    }
}

