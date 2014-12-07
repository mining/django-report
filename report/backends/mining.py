# -*- coding: utf-8 -*-
class Mining(object):
    def get_queryset(self):
        if not self.model:
            raise NotImplementedError("You must provide a 'model' method for "
                                      "the '%r' Open Mining." % self)
