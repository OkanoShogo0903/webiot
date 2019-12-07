set_goal:
	curl http://0.0.0.0:5000/goal -d "x=5&y=10"
mqtt_sub:
	mosquitto_sub -d -t f_team/direction
mqtt_pub:
	mosquitto_pub -d -t f_team/direction -m "100,200"
