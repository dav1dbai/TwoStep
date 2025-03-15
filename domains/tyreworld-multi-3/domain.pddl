(define (domain tyreworld)
(:requirements :typing)
(:types 
    obj - object
    tool wheel nut - obj
    container hub - object
    robot - robot)

(:predicates 
    ;; Container states
    (open ?x - container)
    (closed ?x - container)
    (unlocked ?x - container)
    (in ?x - obj ?y - container)
    
    ;; Hub states
    (on-ground ?x - hub)
    (not-on-ground ?x - hub)
    (fastened ?x - hub)
    (unfastened ?x - hub)
    (free ?x - hub)
    
    ;; Wheel states
    (inflated ?x - wheel)
    (not-inflated ?x - wheel)
    (intact ?x - wheel)
    (on ?x - wheel ?y - hub)
    
    ;; Nut states
    (loose ?x - nut ?y - hub)
    (tight ?x - nut ?y - hub)
    
    ;; Robot states
    (holding ?r - robot ?x - obj)
    (robot-at ?r - robot ?h - hub))

(:action open
    :parameters (?r - robot ?x - container)
    :precondition (and 
        (unlocked ?x)
        (closed ?x))
    :effect (and 
        (open ?x)
        (not (closed ?x))))

(:action close
    :parameters (?r - robot ?x - container)
    :precondition (open ?x)
    :effect (and 
        (closed ?x)
        (not (open ?x))))

(:action fetch
    :parameters (?r - robot ?x - obj ?y - container)
    :precondition (and 
        (in ?x ?y)
        (open ?y)
        (not (exists (?r2 - robot) (holding ?r2 ?x))))
    :effect (and 
        (holding ?r ?x)
        (not (in ?x ?y))))

(:action put-away
    :parameters (?r - robot ?x - obj ?y - container)
    :precondition (and 
        (holding ?r ?x)
        (open ?y))
    :effect (and 
        (in ?x ?y)
        (not (holding ?r ?x))))

(:action loosen
    :parameters (?r - robot ?x - nut ?y - hub)
    :precondition (and 
        (tight ?x ?y)
        (on-ground ?y)
        (robot-at ?r ?y))
    :effect (and 
        (loose ?x ?y)
        (not (tight ?x ?y))))

(:action tighten
    :parameters (?r - robot ?x - nut ?y - hub)
    :precondition (and 
        (loose ?x ?y)
        (on-ground ?y)
        (robot-at ?r ?y))
    :effect (and 
        (tight ?x ?y)
        (not (loose ?x ?y))))

(:action jack-up
    :parameters (?r - robot ?y - hub)
    :precondition (and 
        (on-ground ?y)
        (robot-at ?r ?y))
    :effect (and 
        (not-on-ground ?y)
        (not (on-ground ?y))))

(:action jack-down
    :parameters (?r - robot ?y - hub)
    :precondition (and 
        (not-on-ground ?y)
        (robot-at ?r ?y))
    :effect (and 
        (on-ground ?y)
        (not (not-on-ground ?y))))

(:action undo
    :parameters (?r - robot ?x - nut ?y - hub)
    :precondition (and 
        (not-on-ground ?y)
        (fastened ?y)
        (loose ?x ?y)
        (robot-at ?r ?y)
        (not (exists (?r2 - robot) (holding ?r2 ?x))))
    :effect (and 
        (holding ?r ?x)
        (unfastened ?y)
        (not (fastened ?y))
        (not (loose ?x ?y))))

(:action do-up
    :parameters (?r - robot ?x - nut ?y - hub)
    :precondition (and 
        (unfastened ?y)
        (not-on-ground ?y)
        (holding ?r ?x)
        (robot-at ?r ?y))
    :effect (and 
        (loose ?x ?y)
        (fastened ?y)
        (not (unfastened ?y))
        (not (holding ?r ?x))))

(:action remove-wheel
    :parameters (?r - robot ?x - wheel ?y - hub)
    :precondition (and 
        (not-on-ground ?y)
        (on ?x ?y)
        (unfastened ?y)
        (robot-at ?r ?y)
        (not (exists (?r2 - robot) (holding ?r2 ?x))))
    :effect (and 
        (holding ?r ?x)
        (free ?y)
        (not (on ?x ?y))))

(:action put-on-wheel
    :parameters (?r - robot ?x - wheel ?y - hub)
    :precondition (and 
        (holding ?r ?x)
        (free ?y)
        (unfastened ?y)
        (not-on-ground ?y)
        (robot-at ?r ?y))
    :effect (and 
        (on ?x ?y)
        (not (free ?y))
        (not (holding ?r ?x))))

(:action inflate
    :parameters (?r - robot ?x - wheel)
    :precondition (and 
        (not-inflated ?x)
        (intact ?x)
        (holding ?r ?x))
    :effect (and 
        (inflated ?x)
        (not (not-inflated ?x))))

(:action move
    :parameters (?r - robot ?from ?to - hub)
    :precondition (and 
        (robot-at ?r ?from)
        (not (= ?from ?to)))
    :effect (and 
        (robot-at ?r ?to)
        (not (robot-at ?r ?from))))
)



