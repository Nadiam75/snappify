"""
Server startup script with different configurations
Run this script to start the OCR API server
"""

import uvicorn
import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description="Start OCR API server")
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1, use 1 for OCR models)"
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
        help="Log level (default: info)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Starting OCR API Server")
    print("=" * 60)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Reload: {args.reload}")
    print(f"Workers: {args.workers}")
    print(f"Log Level: {args.log_level}")
    print("=" * 60)
    print(f"\nAPI will be available at: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}")
    print(f"Interactive docs: http://{args.host if args.host != '0.0.0.0' else 'localhost'}:{args.port}/docs")
    print("\nPress CTRL+C to stop the server\n")
    
    uvicorn.run(
        "api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,  # Reload doesn't work with multiple workers
        log_level=args.log_level
    )


if __name__ == "__main__":
    main()

