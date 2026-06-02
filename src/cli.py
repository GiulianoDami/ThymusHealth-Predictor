import argparse
import sys
from typing import Any, Dict

# Import project modules
from src.analyzer import analyze_single_case, run_batch_analysis
from src.utils import load_dicom_series


def setup_parser() -> argparse.ArgumentParser:
    """Set up and return the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="ThymusHealth Predictor - Analyze thymus health from medical imaging data"
    )
    
    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest='mode', help='Analysis mode')
    
    # Single analysis mode
    single_parser = subparsers.add_parser('single', help='Analyze a single DICOM series')
    single_parser.add_argument('input_path', help='Path to DICOM file or directory')
    single_parser.add_argument('--output', '-o', help='Output file path for results')
    
    # Batch processing mode
    batch_parser = subparsers.add_parser('batch', help='Process multiple DICOM series')
    batch_parser.add_argument('input_dir', help='Directory containing DICOM series')
    batch_parser.add_argument('--output', '-o', required=True, help='Output CSV file path')
    batch_parser.add_argument('--recursive', '-r', action='store_true', help='Recursively search directories')
    
    return parser


def run_single_analysis(args: argparse.Namespace) -> None:
    """Run single case analysis."""
    try:
        print(f"Analyzing single case from: {args.input_path}")
        
        # Load DICOM data
        dicom_data = load_dicom_series(args.input_path)
        
        # Perform analysis
        results = analyze_single_case(dicom_data)
        
        # Output results
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to: {args.output}")
        else:
            import json
            print(json.dumps(results, indent=2))
            
    except Exception as e:
        print(f"Error in single analysis: {str(e)}", file=sys.stderr)
        sys.exit(1)


def run_batch_processing(args: argparse.Namespace) -> None:
    """Run batch processing of multiple cases."""
    try:
        print(f"Processing batch from directory: {args.input_dir}")
        
        # Run batch analysis
        results_df = run_batch_analysis(
            args.input_dir,
            recursive=args.recursive
        )
        
        # Save results
        results_df.to_csv(args.output, index=False)
        print(f"Batch results saved to: {args.output}")
        print(f"Processed {len(results_df)} cases")
        
    except Exception as e:
        print(f"Error in batch processing: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point for the CLI."""
    parser = setup_parser()
    args = parser.parse_args()
    
    if not args.mode:
        parser.print_help()
        sys.exit(1)
    
    if args.mode == 'single':
        run_single_analysis(args)
    elif args.mode == 'batch':
        run_batch_processing(args)
    else:
        print(f"Unknown mode: {args.mode}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()