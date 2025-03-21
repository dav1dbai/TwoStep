(define (domain barman)
  (:requirements :strips :typing)
  (:types hand level beverage dispenser container - object
  	  ingredient cocktail - beverage
          shot shaker - container
          robot - robot)

  (:predicates  (ontable ?c - container)
                (holding ?r - robot ?h - hand ?c - container)
		(handempty ?r - robot ?h - hand)
		(empty ?c - container)
                (contains ?c - container ?b - beverage)
		(clean ?c - container)
                (used ?c - container ?b - beverage)
                (dispenses ?d - dispenser ?i - ingredient)
		(shaker-empty-level ?s - shaker ?l - level)
		(shaker-level ?s - shaker ?l - level)
		(next ?l1 ?l2 - level)
		(unshaked ?s - shaker)
		(shaked ?s - shaker)
                (cocktail-part1 ?c - cocktail ?i - ingredient)
                (cocktail-part2 ?c - cocktail ?i - ingredient))
		
  (:action grasp
             :parameters (?r - robot ?h - hand ?c - container)
             :precondition (and (ontable ?c) (handempty ?r ?h))
             :effect (and (not (ontable ?c))
	     	     	  (not (handempty ?r ?h))
			  (holding ?r ?h ?c)))

  (:action leave
             :parameters (?r - robot ?h - hand ?c - container)
             :precondition (holding ?r ?h ?c)
             :effect (and (not (holding ?r ?h ?c))
	     	     	  (handempty ?r ?h)
			  (ontable ?c)))
  
  (:action fill-shot
           :parameters (?r - robot ?s - shot ?i - ingredient ?h1 ?h2 - hand ?d - dispenser)
           :precondition (and (holding ?r ?h1 ?s)
                              (handempty ?r ?h2)
	   		      (dispenses ?d ?i)
                              (empty ?s)
			      (clean ?s))
           :effect (and (not (empty ?s))
	   	   	(contains ?s ?i)
	   	   	(not (clean ?s))
			(used ?s ?i)))


  (:action refill-shot
           :parameters (?r - robot ?s - shot ?i - ingredient ?h1 ?h2 - hand ?d - dispenser)
           :precondition (and (holding ?r ?h1 ?s)	   		      
                              (handempty ?r ?h2)
	   		      (dispenses ?d ?i)
                              (empty ?s)
			      (used ?s ?i))
           :effect (and (not (empty ?s))
                        (contains ?s ?i)))

  (:action empty-shot
           :parameters (?r - robot ?h - hand ?p - shot ?b - beverage)
           :precondition (and (holding ?r ?h ?p)
                              (contains ?p ?b))
           :effect (and (not (contains ?p ?b))
	   	   	(empty ?p)))

  (:action clean-shot
  	   :parameters (?r - robot ?s - shot ?b - beverage ?h1 ?h2 - hand)
           :precondition (and (holding ?r ?h1 ?s)
                              (handempty ?r ?h2)	   		      
			      (empty ?s)
                              (used ?s ?b))
           :effect (and (not (used ?s ?b))
	   	   	(clean ?s)))

  (:action pour-shot-to-clean-shaker
           :parameters (?r - robot ?s - shot ?i - ingredient ?d - shaker ?h1 - hand ?l ?l1 - level)
           :precondition (and (holding ?r ?h1 ?s)
			      (contains ?s ?i)
                              (empty ?d)
	   		      (clean ?d)                              
                              (shaker-level ?d ?l)
                              (next ?l ?l1))
           :effect (and (not (contains ?s ?i))
	   	   	(empty ?s)
			(contains ?d ?i)
                        (not (empty ?d))
			(not (clean ?d))
			(unshaked ?d)
			(not (shaker-level ?d ?l))
			(shaker-level ?d ?l1)))


  (:action pour-shot-to-used-shaker
           :parameters (?r - robot ?s - shot ?i - ingredient ?d - shaker ?h1 - hand ?l ?l1 - level)
           :precondition (and (holding ?r ?h1 ?s)
			      (contains ?s ?i)
                              (unshaked ?d)
                              (shaker-level ?d ?l)
                              (next ?l ?l1))
           :effect (and (not (contains ?s ?i))
                        (contains ?d ?i)
	   	   	(empty ?s)     
  			(not (shaker-level ?d ?l))
			(shaker-level ?d ?l1)))

  (:action empty-shaker
           :parameters (?r - robot ?h - hand ?s - shaker ?b - cocktail ?l ?l1 - level)
           :precondition (and (holding ?r ?h ?s)
                              (contains ?s ?b)
			      (shaked ?s)
			      (shaker-level ?s ?l)
			      (shaker-empty-level ?s ?l1))
           :effect (and (not (shaked ?s))
	   	   	(not (shaker-level ?s ?l))
	   	   	(shaker-level ?s ?l1)
			(not (contains ?s ?b))
	   	   	(empty ?s)))

  (:action clean-shaker
  	   :parameters (?r - robot ?h1 ?h2 - hand ?s - shaker)
           :precondition (and (holding ?r ?h1 ?s)
                              (handempty ?r ?h2)
                              (empty ?s))
           :effect (and (clean ?s)))
  
  (:action shake
  	   :parameters (?r - robot ?b - cocktail ?d1 ?d2 - ingredient ?s - shaker ?h1 ?h2 - hand)
           :precondition (and (holding ?r ?h1 ?s)
                              (handempty ?r ?h2)
			      (contains ?s ?d1)
                              (contains ?s ?d2)
                              (cocktail-part1 ?b ?d1)
			      (cocktail-part2 ?b ?d2)
			      (unshaked ?s))			      
           :effect (and (not (unshaked ?s))
		        (not (contains ?s ?d1))
                        (not (contains ?s ?d2))
	   	   	(shaked ?s)
                        (contains ?s ?b)))

  (:action pour-shaker-to-shot
           :parameters (?r - robot ?b - beverage ?d - shot ?h - hand ?s - shaker ?l ?l1 - level)
           :precondition (and (holding ?r ?h ?s)
			      (shaked ?s)
			      (empty ?d)
			      (clean ?d)
			      (contains ?s ?b)
                              (shaker-level ?s ?l)
                              (next ?l1 ?l))
           :effect (and (not (clean ?d))
	   	   	(not (empty ?d))
			(contains ?d ?b)
			(shaker-level ?s ?l1)
			(not (shaker-level ?s ?l))))
 )