import pandas as pd


class DailyRankingService:

    def __init__(
        self,
        technical_snapshot_service,
        chip_snapshot_service,
        regime_snapshot_service,
        technical_agent,
        chip_agent,
        regime_agent,
        pm_agent,
    ):
        self.technical_snapshot_service = technical_snapshot_service
        self.chip_snapshot_service = chip_snapshot_service
        self.regime_snapshot_service = regime_snapshot_service

        self.technical_agent = technical_agent
        self.chip_agent = chip_agent
        self.regime_agent = regime_agent
        self.pm_agent = pm_agent

    def run(
        self,
        tickers: list[str],
        as_of_date: str,
    ) -> pd.DataFrame:

        regime_data = self.regime_snapshot_service.get_snapshot(
            as_of_date=as_of_date
        )

        regime_report = self.regime_agent.analyze(
            regime_data
        )

        rows = []
        for ticker in tickers:

            technical_data = (
                self.technical_snapshot_service.get_snapshot(
                    ticker=ticker,
                    as_of_date=as_of_date,
                )
            )

            chip_data = (
                self.chip_snapshot_service.get_snapshot(
                    ticker=ticker,
                    as_of_date=as_of_date,
                )
            )

            technical_report = self.technical_agent.analyze(
                technical_data
            )

            chip_report = self.chip_agent.analyze(
                chip_data
            )

            analysis_data = {
                "technical_score": technical_report.score,
                "technical_reason": technical_report.reason,

                "chip_score": chip_report.score,
                "chip_reason": chip_report.reason,

                "market_regime": regime_report.regime,
                "regime_risk_score": regime_report.risk_score,
                "regime_confidence": regime_report.confidence,
                "regime_summary": regime_report.summary,
            }

            pm_report = self.pm_agent.analyze(
                    analysis_data
                )
            rows.append(
                {
                    "as_of_date": as_of_date,
                    "ticker": ticker,

                    "technical_score": technical_report.score,
                    "chip_score": chip_report.score,

                    "regime": regime_report.regime,
                    "regime_score": regime_report.risk_score,
                    "regime_confidence": regime_report.confidence,

                    "final_score": pm_report.final_score,
                    "conviction": pm_report.conviction,
                }
            )

        df = pd.DataFrame(rows)

        df = (
            df
            .sort_values(
                ["final_score", "conviction", "ticker"],
                ascending=[False, False, True],
            )
            .reset_index(drop=True)
        )

        df["rank"] = range(1, len(df) + 1)

        return df