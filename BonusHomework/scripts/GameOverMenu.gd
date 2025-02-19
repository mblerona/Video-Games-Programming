extends Control

@onready var game_over_label: Label = $GameOverLabel
@onready var restart_button: Button = $VBoxContainer/RestartButton
@onready var quit_button: Button = $VBoxContainer/QuitButton

func _ready() -> void:
	print("GameOverMenu Loaded!")  # Debugging
	if not game_over_label:
		print("Error: GameOverLabel not found!")
	if not restart_button:
		print("Error: RestartButton not found!")
	if not quit_button:
		print("Error: QuitButton not found!")

	visible = false  # Ensure it's hidden at start
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)

	# ✅ Ensure UI receives mouse clicks
	mouse_filter = Control.MOUSE_FILTER_STOP

	# ✅ Debug if clicks are being detected
	connect("gui_input", Callable(self, "_on_gui_input"))

	# Connect buttons
	restart_button.connect("pressed", Callable(self, "_on_restart_pressed"))
	quit_button.connect("pressed", Callable(self, "_on_quit_pressed"))

func show_game_over(message: String) -> void:
	print("Showing Game Over Menu!")  # Debugging

	if game_over_label:
		game_over_label.text = message
	else:
		print("Error: Cannot set GameOverLabel text - Label not found!")

	visible = true  # ✅ Ensure it's visible
	modulate.a = 1  # ✅ Force visibility (fixes transparency issues)
	set_process(true)  # ✅ Ensure it's actively processed
	set_physics_process(true)

	# ✅ Debugging print
	print("GameOverMenu visibility:", visible, " Alpha:", modulate.a)

	get_tree().paused = false  # ✅ Allow UI interaction even if game is paused
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)

func _on_gui_input(event):
	if event is InputEventMouseButton:
		print("Mouse clicked inside Game Over Menu!")

func _on_restart_pressed() -> void:
	print("Restarting game...")  # Debugging
	get_tree().paused = false  # Unpause before restart
	#get_tree().reload_current_scene()  # Restart the game
	
	visible = false 
	var game_manager = get_node("/root/floor/UI")
	if game_manager:
		game_manager.start_game()
	else:
		print("Error: GameManager not found!")
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Lock mouse after restart

func _on_quit_pressed() -> void:
	print("Quitting game...")  # Debugging
	get_tree().quit()
