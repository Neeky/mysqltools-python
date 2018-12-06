from .base import InnodbStatus,InnodbStatusLog


class LogSequenceNumber(InnodbStatusLog):
    dimension = "Log sequence number"

class LogFlushedUpTo(InnodbStatusLog):
    dimension = "Log flushed up to"

class PagesFlushedUpTo(InnodbStatusLog):
    dimension = "Pages flushed up to"

class LastCheckpointAt(InnodbStatusLog):
    dimension = "Last checkpoint at"

        