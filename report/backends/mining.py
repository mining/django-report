# -*- coding: utf-8 -*-
class Mining(object):
    def get_queryset(self):
        if not getattr(self, "model", None):
            raise NotImplementedError("You must provide a 'model' method for "
                                      "the '%r' Open Mining." % self)
