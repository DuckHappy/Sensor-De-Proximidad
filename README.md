<h1> Proyecto Informatico - UNLAM - Sistemas Embebidos <h1>

<h4> Componentes: ESP32  - Sensor de distancia ultrasónico HC-SR04 - LED o Buzzer</h4>
<br>
<h4>Descripcion : El ESP32 mide la distancia usando el sensor ultrasónico HC-SR04. Publica la distancia en un tópico MQTT. Un dashboard (io.adafruit.com) monitoriza la distancia medida. El dashboard(io.adafruit.com) puede enviar comandos para activar/desactivar la alerta de proximidad a través de MQTT. El ESP32 suscribe a este comando y enciende el LED o el buzzer si la distancia medida es menor a un valor umbral.A ultimo momento se agrego un display que muestra la distancia del momento </h4>
