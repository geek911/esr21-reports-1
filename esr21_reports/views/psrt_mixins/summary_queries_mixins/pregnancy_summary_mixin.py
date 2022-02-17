class PregnancySummaryMixin:
    
    @property
    def no_preg_results_statistics(self):
        """
        No pregnancy result and F and child bearing potential    
        """
        return ["No pregnancy result and F and child bearing potential", 0, 0, 0, 0, 0, 0]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update(
            no_preg_results_stats = self.no_preg_results_statistics,
        )

        return context
        