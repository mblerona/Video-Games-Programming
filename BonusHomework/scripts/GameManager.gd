

extends Node

@export var total_time: float = 30.0
@export var required_treasure: int = 2

var collected: int = 0
var time_left: float = 0.0
var player_start_position: Vector3  

@onready var timer_label: Label = $CanvasLayer/TimerLabel
@onready var treasure_label: Label = $CanvasLayer/TreasureLabel
@onready var game_ui: CanvasLayer = $CanvasLayer  # Reference to the entire UI
@onready var game_over_menu = get_node("/root/floor/GameOverMenu")  # ✅ Direct reference to GameOverMenu
@onready var player = get_node("/root/floor/Player")

func _ready() -> void:
	print("GameManager Loaded!")  # ✅ Debugging
	time_left = total_time
	update_labels()
	connect_coins()
	game_ui.visible = false  # Ensure UI is hidden at the start

	# ✅ Save player's initial position
	if player:
		player_start_position = player.global_transform.origin

func connect_coins():
	var coins = get_tree().get_nodes_in_group("Coins")  # ✅ Find all coins in scene

	for coin in coins:
		if coin.has_signal("coin_collected"):  # ✅ Check if signal exists
			if not coin.is_connected("coin_collected", self.add_treasure):
				coin.connect("coin_collected", self.add_treasure)  # ✅ Connect signal
			print("✅ Connected coin at", coin.global_transform.origin, "to GameManager.")
		else:
			print("⚠️ Error: Coin at", coin.global_transform.origin, "is missing 'coin_collected' signal!")

	print("Connected", len(coins), "coins to GameManager.")  # ✅ Debugging

func start_game() -> void:
	print("Game started!")  # ✅ Debugging check
	game_ui.visible = true
	if game_over_menu:
		game_over_menu.visible = false
	get_tree().paused = false
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	time_left = total_time
	collected = 0
	update_labels()

	# ✅ Reset player position and collision when restarting
	if player:
		player.global_transform.origin = player_start_position  # Move back to start
		var collider = player.get_node("CollisionShape3D")
		if collider:
			collider.disabled = false  # Re-enable collision

func _process(delta: float) -> void:
	if game_ui.visible:
		time_left -= delta

		# Start blinking in the last 5 seconds
		if time_left <= 5 and time_left > 1 and player:
			var blink_rate = 5  # Blink every 0.5 seconds
			player.visible = int(time_left * blink_rate) % 2 == 0

		# Disable collision in the last second
		if time_left <= 1 and player:
			player.visible = true  # Ensure visibility before falling
			var collider = player.get_node("CollisionShape3D")
			if collider:
				collider.disabled = true  # Turn off collision

		if time_left <= 0:
			time_left = 0
			game_over("Time's up! Game Over.")
			
		update_labels()
		
func update_labels() -> void:
	if treasure_label:
		treasure_label.text = "Treasures: " + str(collected) + " / " + str(required_treasure)
	if timer_label:
		timer_label.text = "Time Left: " + str(round(time_left))
		if time_left <= 10:
			timer_label.add_theme_color_override("font_color", Color.RED)
		else:
			timer_label.add_theme_color_override("font_color", Color.WHITE)

func add_treasure() -> void:
	collected += 1
	update_labels()
	print("Treasure collected! New count:", collected)  # ✅ Debugging print
	if collected >= required_treasure:
		game_over("Congratulations, you won!")

func game_over(message: String) -> void:
	print(message)
	game_ui.visible = false
	if game_over_menu:
		game_over_menu.visible = true
		game_over_menu.modulate.a = 1
		game_over_menu.call("show_game_over", message)
	get_tree().paused = false
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
