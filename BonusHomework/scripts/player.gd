##extends CharacterBody3D
##
##const BASE_SPEED = 7.0
##const SPRINT_SPEED = 12.0  # Speed when holding "X"
##const JUMP_VELOCITY = 4.5
##const DOUBLE_JUMP_VELOCITY = 7.0  # Higher jump on second press
##const MOUSE_SENSITIVITY = 0.2  # Adjust for faster/slower rotation
##
##var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")  # Get Godot's gravity value
##var pitch: float = 0.0  # Controls vertical camera rotation
##var can_double_jump: bool = false  # Tracks if player can double jump
##var speed: float = BASE_SPEED  # Current movement speed
##
##@onready var camera = $Camera3D  # Ensure this matches your scene setup
##
##func _ready():
	##add_to_group("Player")  # Ensures the player is in the group
	##
	### **Only capture mouse when game starts**
	##if get_tree().current_scene.name == "MainMenu" or get_tree().paused:
		##Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Mouse visible in menu
	##else:
		##Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Mouse captured in game
##
##func _physics_process(delta: float) -> void:
	### Apply gravity if the player is not on the floor
	##if not is_on_floor():
		##velocity.y -= gravity * delta
##
	### Handle jumping
	##if Input.is_action_just_pressed("jump"):
		##if is_on_floor():
			##velocity.y = JUMP_VELOCITY
			##can_double_jump = true  # Allow double jump after first jump
		##elif can_double_jump:
			##velocity.y = DOUBLE_JUMP_VELOCITY
			##can_double_jump = false  # Disable double jump after using it
##
	### **Sprint Handling**
	##if Input.is_action_pressed("run"):  # Holding "X" increases speed
		##speed = SPRINT_SPEED
	##else:
		##speed = BASE_SPEED
##
	### **Movement Handling**
	##var direction = Vector3.ZERO
##
	##if Input.is_action_pressed("move_forward"):
		##direction.z -= 1
	##if Input.is_action_pressed("move_backward"):
		##direction.z += 1
	##if Input.is_action_pressed("move_left"):
		##direction.x -= 1
	##if Input.is_action_pressed("move_right"):
		##direction.x += 1
##
	### Convert local direction to world direction
	##direction = transform.basis * direction
	##direction.y = 0  # Prevent vertical movement
##
	### Apply movement speed
	##if direction != Vector3.ZERO:
		##velocity.x = direction.normalized().x * speed
		##velocity.z = direction.normalized().z * speed
	##else:
		##velocity.x = move_toward(velocity.x, 0, speed)
		##velocity.z = move_toward(velocity.z, 0, speed)
##
	### Move the player
	##move_and_slide()
##
##func _input(event):
	### **Escape Key - Release Mouse & Quit (Only in Game)**
	##if event.is_action_pressed("ui_cancel"):
		##Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse
		##print("Mouse unlocked!")
##
	### **Middle Mouse Button - Toggle Free Look (Only in Game)**
	##if event is InputEventMouseButton:
		##if event.button_index == MOUSE_BUTTON_MIDDLE and get_tree().current_scene.name != "MainMenu":
			##if event.pressed:
				##Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Lock mouse when pressed
			##else:
				##Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse when released
##
	### **Mouse Look - Only While Holding Middle Mouse Button**
	##if event is InputEventMouseMotion and Input.is_action_pressed("toggle_mouse"):
		##rotate_y(deg_to_rad(-event.relative.x * MOUSE_SENSITIVITY))  # Rotate player left/right
		##pitch = clamp(pitch - event.relative.y * MOUSE_SENSITIVITY, -80, 80)  # Clamp vertical rotation
		##camera.rotation_degrees.x = pitch  # Apply vertical rotation to camera
#
#
#extends CharacterBody3D
#
#const BASE_SPEED = 7.0
#const SPRINT_SPEED = 12.0  # Speed when holding "X"
#const JUMP_VELOCITY = 4.5
#const DOUBLE_JUMP_VELOCITY = 7.0  # Higher jump on second press
#const MOUSE_SENSITIVITY = 0.2  # Adjust for faster/slower rotation
#
#var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")  # Get Godot's gravity value
#var pitch: float = 0.0  # Controls vertical camera rotation
#var can_double_jump: bool = false  # Tracks if player can double jump
#var speed: float = BASE_SPEED  # Current movement speed
#
#@onready var camera = $Camera3D  # Ensure this matches your scene setup
#@onready var animation_player = $AnimationPlayer  # ✅ Reference to AnimationPlayer
#
#func _ready():
	#add_to_group("Player")  # Ensures the player is in the group
	#
	## **Only capture mouse when game starts**
	#if get_tree().current_scene.name == "MainMenu" or get_tree().paused:
		#Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Mouse visible in menu
	#else:
		#Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Mouse captured in game
#
#func _physics_process(delta: float) -> void:
	## Apply gravity if the player is not on the floor
	#if not is_on_floor():
		#velocity.y -= gravity * delta
#
	## Handle jumping
	#if Input.is_action_just_pressed("jump"):
		#if is_on_floor():
			#velocity.y = JUMP_VELOCITY
			#can_double_jump = true  # Allow double jump after first jump
		#elif can_double_jump:
			#velocity.y = DOUBLE_JUMP_VELOCITY
			#can_double_jump = false  # Disable double jump after using it
#
	## **Sprint Handling**
	#if Input.is_action_pressed("run"):  # Holding "X" increases speed
		#speed = SPRINT_SPEED
	#else:
		#speed = BASE_SPEED
#
	## **Movement Handling**
	#var direction = Vector3.ZERO
	#var is_moving = false  # ✅ Track movement state
#
	#if Input.is_action_pressed("move_forward"):
		#direction.z -= 1
		#is_moving = true
	#if Input.is_action_pressed("move_left"):
		#direction.x -= 1
		#is_moving = true
	#if Input.is_action_pressed("move_right"):
		#direction.x += 1
		#is_moving = true
	#if Input.is_action_pressed("move_backward"):
		#direction.z += 1
		#is_moving=true
#
	## Convert local direction to world direction
	#direction = transform.basis * direction
	#direction.y = 0  # Prevent vertical movement
#
	## Apply movement speed
	#if direction != Vector3.ZERO:
		#velocity.x = direction.normalized().x * speed
		#velocity.z = direction.normalized().z * speed
	#else:
		#velocity.x = move_toward(velocity.x, 0, speed)
		#velocity.z = move_toward(velocity.z, 0, speed)
#
	## **Play Walk Animation**
	#if is_moving:
		#if not animation_player.is_playing() or animation_player.current_animation != "walk":
			#animation_player.play("walk")  # ✅ Play walk animation
	#else:
		#if animation_player.current_animation == "walk":
			#animation_player.stop()  # ✅ Stop walking animation when player stops
#
	## Move the player
	#move_and_slide()
#
#func _input(event):
	## **Escape Key - Release Mouse & Quit (Only in Game)**
	#if event.is_action_pressed("ui_cancel"):
		#Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse
		#print("Mouse unlocked!")
#
	## **Middle Mouse Button - Toggle Free Look (Only in Game)**
	#if event is InputEventMouseButton:
		#if event.button_index == MOUSE_BUTTON_MIDDLE and get_tree().current_scene.name != "MainMenu":
			#if event.pressed:
				#Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Lock mouse when pressed
			#else:
				#Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse when released
#
	## **Mouse Look - Only While Holding Middle Mouse Button**
	#if event is InputEventMouseMotion and Input.is_action_pressed("toggle_mouse"):
		#rotate_y(deg_to_rad(-event.relative.x * MOUSE_SENSITIVITY))  # Rotate player left/right
		#pitch = clamp(pitch - event.relative.y * MOUSE_SENSITIVITY, -80, 80)  # Clamp vertical rotation
		#camera.rotation_degrees.x = pitch  # Apply vertical rotation to camera


extends CharacterBody3D

const BASE_SPEED = 7.0
const SPRINT_SPEED = 12.0  
const JUMP_VELOCITY = 4.5
const DOUBLE_JUMP_VELOCITY = 7.0 
const MOUSE_SENSITIVITY = 0.2  

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")  # Get Godot's gravity value
var pitch: float = 0.0 
var can_double_jump: bool = false  
var speed: float = BASE_SPEED  

@onready var camera = $Camera3D  # Ensure this matches your scene setup
@onready var animation_player = $AnimationPlayer  # ✅ Reference to AnimationPlayer

func _ready():
	add_to_group("Player")  # Ensures the player is in the group
	
	# **Only capture mouse when game starts**
	if get_tree().current_scene.name == "MainMenu" or get_tree().paused:
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Mouse visible in menu
	else:
		Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Mouse captured in game

func _physics_process(delta: float) -> void:
	# Apply gravity if the player is not on the floor
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Handle jumping
	if Input.is_action_just_pressed("jump"):
		if is_on_floor():
			velocity.y = JUMP_VELOCITY
			can_double_jump = true  # Allow double jump after first jump
			animation_player.play("Jump/mixamo_com")  # ✅ Play jump animation
		elif can_double_jump:
			velocity.y = DOUBLE_JUMP_VELOCITY
			can_double_jump = false  # Disable double jump after using it
			animation_player.play("Jump/mixamo_com")  # ✅ Play jump animation again

	# **Sprint Handling**
	var is_sprinting = false
	if Input.is_action_pressed("run"):  # Holding "X" increases speed
		speed = SPRINT_SPEED
		is_sprinting = true
	else:
		speed = BASE_SPEED

	# **Movement Handling**
	var direction = Vector3.ZERO
	var is_moving = false  # ✅ Track movement state

	if Input.is_action_pressed("move_forward"):
		direction.z -= 1
		is_moving = true
	if Input.is_action_pressed("move_left"):
		direction.x -= 1
		is_moving = true
	if Input.is_action_pressed("move_right"):
		direction.x += 1
		is_moving = true
	if Input.is_action_pressed("move_backward"):
		direction.z += 1
		is_moving=true

	# Convert local direction to world direction
	direction = transform.basis * direction
	direction.y = 0  # Prevent vertical movement

	# Apply movement speed
	if direction != Vector3.ZERO:
		velocity.x = direction.normalized().x * speed
		velocity.z = direction.normalized().z * speed
	else:
		velocity.x = move_toward(velocity.x, 0, speed)
		velocity.z = move_toward(velocity.z, 0, speed)

	# **Animation Handling**
	if is_moving:
		if is_sprinting:
			if not animation_player.is_playing() or animation_player.current_animation != "Fast Run (1)/mixamo_com":
				animation_player.play("Fast Run (1)/mixamo_com")  # ✅ Play fast run animation
		else:
			if not animation_player.is_playing() or animation_player.current_animation != "walk":
				animation_player.play("Walking (1)/mixamo_com")  # ✅ Play walk animation
	else:
		if animation_player.current_animation == "walk" or animation_player.current_animation == "Fast Run (1)/mixamo_com":
			animation_player.stop()  # ✅ Stop walk/run animation when player stops

	# Move the player
	move_and_slide()

func _input(event):
	# **Escape Key - Release Mouse & Quit (Only in Game)**
	if event.is_action_pressed("ui_cancel"):
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse
		print("Mouse unlocked!")

	# **Middle Mouse Button - Toggle Free Look (Only in Game)**
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_MIDDLE and get_tree().current_scene.name != "MainMenu":
			if event.pressed:
				Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)  # Lock mouse when pressed
			else:
				Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)  # Unlock mouse when released

	# **Mouse Look - Only While Holding Middle Mouse Button**
	if event is InputEventMouseMotion and Input.is_action_pressed("toggle_mouse"):
		rotate_y(deg_to_rad(-event.relative.x * MOUSE_SENSITIVITY))  # Rotate player left/right
		pitch = clamp(pitch - event.relative.y * MOUSE_SENSITIVITY, -80, 80)  # Clamp vertical rotation
		camera.rotation_degrees.x = pitch  # Apply vertical rotation to camera
