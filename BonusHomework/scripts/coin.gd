#extends Area3D
#
#@export var amplitude: float = 0.5  # How high the coin floats up/down
#@export var float_speed: float = 2.0  # Speed of the floating animation
#
#var base_y: float  # The starting Y position
#var elapsed_time: float = 0.0  # Accumulated time for animation
#
#signal coin_collected  # ✅ Signal to notify GameManager
#
#func _ready() -> void:
	#base_y = global_transform.origin.y
	#connect("body_entered", Callable(self, "_on_body_entered"))  # ✅ Detect player collecting coin
#
#func _process(delta: float) -> void:
	#elapsed_time += delta
	#var offset = sin(elapsed_time * float_speed) * amplitude
	#var new_pos = global_transform.origin
	#new_pos.y = base_y + offset
	#global_transform.origin = new_pos
#
#func _on_body_entered(body: Node) -> void:
	#if body.is_in_group("Player"):
		#print("Coin collected!")  # ✅ Debugging print
		#
		## ✅ Find GameManager inside `floor.tscn`
		#
		#var gm = get_node("/root/floor/UI")
#
		#if gm:
			#gm.add_treasure()  # ✅ Directly call add_treasure()
			#print("GameManager found! add_treasure() called.")  # ✅ Debugging print
		#else:
			#print("Error: GameManager not found in scene!")  # ❌ Debugging print
#
		#emit_signal("coin_collected")  # ✅ Emit signal for external listeners
		#queue_free()  # ✅ Remove coin from scene after collection


extends Area3D

@export var amplitude: float = 0.5  # How high the coin floats up/down
@export var float_speed: float = 2.0  # Speed of the floating animation

var base_y: float  # The starting Y position
var elapsed_time: float = 0.0  # Accumulated time for animation

signal coin_collected  # ✅ Signal to notify GameManager

func _ready() -> void:
	base_y = global_transform.origin.y
	connect("body_entered", Callable(self, "_on_body_entered"))  # ✅ Detect player collecting coin

func _process(delta: float) -> void:
	elapsed_time += delta
	var offset = sin(elapsed_time * float_speed) * amplitude
	var new_pos = global_transform.origin
	new_pos.y = base_y + offset
	global_transform.origin = new_pos

func _on_body_entered(body: Node) -> void:
	if body.is_in_group("Player"):
		print("Coin collected!")  
		
		
		
		emit_signal("coin_collected")  #  Emit signal for GameManager to handle
		queue_free()  #  Remove coin from scene after collection
