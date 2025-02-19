extends Control

@onready var start_button = $VBoxContainer/StartButton
@onready var quit_button = $VBoxContainer/QuitButton
@onready var game_manager = get_node("/root/floor/UI")  # Find GameManager in the scene

func _ready() -> void:
	visible = true  
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Ensure cursor is visible

func _on_start_button_pressed() -> void:
	print("Start button clicked!")  
	visible = false  # Hide menu
	get_tree().paused = false  # Resume game
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Lock cursor for gameplay

	# Ensure UI is visible and game starts
	if game_manager:
		game_manager.start_game()
	else:
		print("Error: GameManager not found!")

func _on_quit_button_pressed() -> void:
	print("Quit button clicked!")  
	get_tree().quit()
