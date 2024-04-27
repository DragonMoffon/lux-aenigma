"""
A system agnostic way for one-way non-authoritative communication between systems.

Notifications are serializable singleton objects.
Creating a Notification with the same signature will return the same reference in memory
from the Notifier within the same Namespace. Any object may attach one or more callbacks to the
Notification as long as the callbacks match the signature of the Notification. Depending on how
the Notification was first defined it can be emitted by either only the first parent, or by any
reference to the notification. There is no promise to the order in which the callbacks are made.
Notifications can be serialised, and loaded from disk at run time. This allows for the
front-loading of Notification creation.

Some extra notes:
    - Unlike Pyglet's events Notifications do not need to be emitted from a particular source.
This allows for many to one, one to many, and many to many communication.
    - use the `**kwargs` syntax if a callback does not need every argument of the Notification
    - Notifications can also store values to pass into callbacks. These cannot be overridden at emit time
    - Notifications make no claims to a callback so it can be used by multiple notifications
    - Notifications hold only weak references to callbacks so callbacks will automatically be freed
on destruction. This also means you should only keep a long living reference to a Notification
if you will repeatedly subscribe or unsubscribe, or you plan to emit the Notification.
    - a Callback may return values, but they will be ignored by the Notification.
    - Notifications have multiple levels of debugging to help clarify data flow.
This can go all the way to sys shenanigans to mark the line it was emitted from, and the parent object.
    - Unsurprisingly Notifications use metaclass shenanigans so take care when attempting to extend them.
    - [Maybe] With a Notifier in Async mode emitting a Notification is thread safe. This does not mean
callbacks are thread safe. That is up to you as the user.

Notifiers are the responsible for storing references to Notifications and delegating their references out.
Every Notifier has an allocated namespace. Notifications with an invalid namespace will have a hissy-fit.
By default, the namespace of a Notifier and Notification is the module it was created in. Much like
Notifications Notifiers are serializable. They can be Serialised explicitly or created automatically for
any unassigned namespace referenced by a Notification. This second behaviour is on by default but can be
disabled. In which case unassigned namespaces will raise errors. An important configuration for Notifiers
is their emit mode. In `immediate` mode they will release an emitted Notification to callbacks instantly,
in `gate` mode the notifications will be stored in a stack and then the Notifier must be told when to release
them. For example this mode allows you to call all notifications at the start of on_update. `Async` mode
forces emitted Notifications into a thread safe queue to be called atomically. [Note I don't know how possible this is]
"""
class _NotificationSignature:
    pass

    def __hash__(self):
        pass

    def __eq__(self, other):
        pass


class Notifier:
    pass


class Notification:
    pass
