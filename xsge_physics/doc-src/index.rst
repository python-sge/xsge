**********************
xSGE Physics Framework
**********************

.. This file has been dedicated to the public domain, to the extent
   possible under applicable law, via CC0. See
   http://creativecommons.org/publicdomain/zero/1.0/ for more
   information. This file is offered as-is, without any warranty.

.. contents::

.. automodule:: xsge_physics

xsge_physics Classes
====================

xsge_physics.Collider
---------------------

.. autoclass:: xsge_physics.Collider

xsge_physics.Collider Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.Collider.move_x

.. automethod:: xsge_physics.Collider.move_y

.. automethod:: xsge_physics.Collider.get_left_touching_wall

.. automethod:: xsge_physics.Collider.get_right_touching_wall

.. automethod:: xsge_physics.Collider.get_top_touching_wall

.. automethod:: xsge_physics.Collider.get_bottom_touching_wall

.. automethod:: xsge_physics.Collider.get_left_touching_slope

.. automethod:: xsge_physics.Collider.get_right_touching_slope

.. automethod:: xsge_physics.Collider.get_top_touching_slope

.. automethod:: xsge_physics.Collider.get_bottom_touching_slope

xsge_physics.Collider Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.Collider.event_physics_collision_left

.. automethod:: xsge_physics.Collider.event_physics_collision_right

.. automethod:: xsge_physics.Collider.event_physics_collision_top

.. automethod:: xsge_physics.Collider.event_physics_collision_bottom

xsge_physics.Wall
-----------------

.. autoclass:: xsge_physics.Wall

xsge_physics.SolidLeft
----------------------

.. autoclass:: xsge_physics.SolidLeft

xsge_physics.SolidLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SolidLeft.event_physics_collision_left

xsge_physics.SolidRight
-----------------------

.. autoclass:: xsge_physics.SolidRight

xsge_physics.SolidRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SolidRight.event_physics_collision_right

xsge_physics.SolidTop
---------------------

.. autoclass:: xsge_physics.SolidTop

xsge_physics.SolidTop Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SolidTop.event_physics_collision_top

xsge_physics.SolidBottom
------------------------

.. autoclass:: xsge_physics.SolidBottom

xsge_physics.SolidBottom Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SolidBottom.event_physics_collision_bottom

xsge_physics.Solid
------------------

.. autoclass:: xsge_physics.Solid

xsge_physics.Solid Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.Solid.event_physics_collision_left

.. automethod:: xsge_physics.Solid.event_physics_collision_right

.. automethod:: xsge_physics.Solid.event_physics_collision_top

.. automethod:: xsge_physics.Solid.event_physics_collision_bottom

xsge_physics.Slope
------------------

.. autoclass:: xsge_physics.Slope

xsge_physics.SlopeTopLeft
-------------------------

.. autoclass:: xsge_physics.SlopeTopLeft

xsge_physics.SlopeTopLeft Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeTopLeft.get_slope_x
.. automethod:: xsge_physics.SlopeTopLeft.get_slope_y

xsge_physics.SlopeTopLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeTopLeft.event_physics_collision_left

.. automethod:: xsge_physics.SlopeTopLeft.event_physics_collision_top

xsge_physics.SlopeTopRight
--------------------------

.. autoclass:: xsge_physics.SlopeTopRight

xsge_physics.SlopeTopRight Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeTopRight.get_slope_x
.. automethod:: xsge_physics.SlopeTopRight.get_slope_y

xsge_physics.SlopeTopRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeTopRight.event_physics_collision_right

.. automethod:: xsge_physics.SlopeTopRight.event_physics_collision_top

xsge_physics.SlopeBottomLeft
----------------------------

.. autoclass:: xsge_physics.SlopeBottomLeft

xsge_physics.SlopeBottomLeft Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeBottomLeft.get_slope_x
.. automethod:: xsge_physics.SlopeBottomLeft.get_slope_y

xsge_physics.SlopeBottomLeft Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeBottomLeft.event_physics_collision_left

.. automethod:: xsge_physics.SlopeBottomLeft.event_physics_collision_bottom

xsge_physics.SlopeBottomRight
-----------------------------

.. autoclass:: xsge_physics.SlopeBottomRight

xsge_physics.SlopeBottomRight Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeBottomRight.get_slope_x
.. automethod:: xsge_physics.SlopeBottomRight.get_slope_y

xsge_physics.SlopeBottomRight Event Methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.SlopeBottomRight.event_physics_collision_right

.. automethod:: xsge_physics.SlopeBottomRight.event_physics_collision_bottom

xsge_physics.MobileWall
-----------------------

.. autoclass:: xsge_physics.MobileWall

xsge_physics.MobileWall methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automethod:: xsge_physics.MobileWall.get_stuck_colliders

.. automethod:: xsge_physics.MobileWall.move_x

.. automethod:: xsge_physics.MobileWall.move_y

xsge_physics.MobileColliderWall
-------------------------------

.. autoclass:: xsge_physics.MobileColliderWall
