from django.db import models
import logging

class Alias(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)

    def __unicode__(self):
        return unicode(self.source)+' -> '+unicode(self.destination)

    class Meta:
        ordering = ['source', 'destination']
        verbose_name = 'alias'
        verbose_name_plural = verbose_name + 'er'
        unique_together = (('source', 'destination'),)

    def json_of(self):
        return {
            'source': self.source,
            'destination': self.destination,
        }

def transitive_closure(u, edges, visited=None):
    if not isinstance(u, basestring):
        res = {}
        for uu in u:
            res[uu] = transitive_closure(uu, edges)
        return res

    if visited:
        visited = frozenset([u]).union(visited)
    else:
        visited = frozenset([u])

    result = frozenset([u])

    if u not in edges:
        return result

    for v in edges[u]:
        if v in visited:
            logging.warning("Cycle involving "+v)
        else:
            result = result.union(transitive_closure(v, edges, visited))

    return result

def resolve_alias(recipient):
    """Given a recipient, return the transitive closure of the alias graph."""
    aliases = {}
    for a in Alias.objects.all():
        if a.source not in aliases:
            aliases[a.source] = set()
        aliases[a.source].add(a.destination)

    return transitive_closure(recipient, aliases)

def resolve_alias_reversed(destination):
    """Given a destination, return all the recipients whose mail will be
    delivered to the destination."""
    aliases = {}
    for a in Alias.objects.all():
        if a.destination not in aliases:
            aliases[a.destination] = set()
        aliases[a.destination].add(a.source)

    return transitive_closure(destination, aliases)
