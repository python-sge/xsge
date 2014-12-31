************
xsge.physics
************

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

.. automodule:: xsge.physics

xsge.physics Classes
====================

xsge.physics.Collider
---------------------

.. autoclass:: xsge.physics.Collider

xsge.physics.Collider Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.Collider.move_x

.. automethod:: xsge.physics.Collider.move_y

.. automethod:: xsge.physics.Collider.get_left_touching_wall

.. automethod:: xsge.physics.Collider.get_right_touching_wall

.. automethod:: xsge.physics.Collider.get_top_touching_wall

.. automethod:: xsge.physics.Collider.get_bottom_touching_wall

.. automethod:: xsge.physics.Collider.get_left_touching_slope

.. automethod:: xsge.physics.Collider.get_right_touching_slope

.. automethod:: xsge.physics.Collider.get_top_touching_slope

.. automethod:: xsge.physics.Collider.get_bottom_touching_slope

xsge.physics.Collider Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.Collider.event_physics_collision_left

.. automethod:: xsge.physics.Collider.event_physics_collision_right

.. automethod:: xsge.physics.Collider.event_physics_collision_top

.. automethod:: xsge.physics.Collider.event_physics_collision_bottom

xsge.physics.SolidLeft
----------------------

.. autoclass:: xsge.physics.SolidLeft

xsge.physics.SolidLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SolidLeft.event_physics_collision_left

xsge.physics.SolidRight
-----------------------

.. autoclass:: xsge.physics.SolidRight

xsge.physics.SolidRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SolidRight.event_physics_collision_right

xsge.physics.SolidTop
---------------------

.. autoclass:: xsge.physics.SolidTop

xsge.physics.SolidTop Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SolidTop.event_physics_collision_top

xsge.physics.SolidBottom
------------------------

.. autoclass:: xsge.physics.SolidBottom

xsge.physics.SolidBottom Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SolidBottom.event_physics_collision_bottom

xsge.physics.Solid
------------------

.. autoclass:: xsge.physics.Solid

xsge.physics.Solid Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.Solid.event_physics_collision_left

.. automethod:: xsge.physics.Solid.event_physics_collision_right

.. automethod:: xsge.physics.Solid.event_physics_collision_top

.. automethod:: xsge.physics.Solid.event_physics_collision_bottom

xsge.physics.SlopeTopLeft
-------------------------

.. autoclass:: xsge.physics.SlopeTopLeft

xsge.physics.SlopeTopLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SlopeTopLeft.event_physics_collision_left

.. automethod:: xsge.physics.SlopeTopLeft.event_physics_collision_top

xsge.physics.SlopeTopRight
--------------------------

.. autoclass:: xsge.physics.SlopeTopRight

xsge.physics.SlopeTopRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SlopeTopRight.event_physics_collision_right

.. automethod:: xsge.physics.SlopeTopRight.event_physics_collision_top

xsge.physics.SlopeBottomLeft
----------------------------

.. autoclass:: xsge.physics.SlopeBottomLeft

xsge.physics.SlopeBottomLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SlopeBottomLeft.event_physics_collision_left

.. automethod:: xsge.physics.SlopeBottomLeft.event_physics_collision_bottom

xsge.physics.SlopeBottomRight
-----------------------------

.. autoclass:: xsge.physics.SlopeBottomRight

xsge.physics.SlopeBottomRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.SlopeBottomRight.event_physics_collision_right

.. automethod:: xsge.physics.SlopeBottomRight.event_physics_collision_bottom

xsge.physics.MobileWall
-----------------------

.. autoclass:: xsge.physics.MobileWall

xsge.physics.MobileWall methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge.physics.MobileWall.get_stuck_colliders

.. automethod:: xsge.physics.MobileWall.move_x

.. automethod:: xsge.physics.MobileWall.move_y
