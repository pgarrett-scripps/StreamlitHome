import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class App:
    title: str
    description: str
    url: str
    category: str
    emoji: str

class AppLoader:
    @staticmethod
    def load_from_yaml(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)

            # Separate categories and apps
            categories = config.get('categories', {})
            apps = [App(**app_data) for app_data in config['apps']]

            return {
                'categories': categories,
                'apps': apps
            }

    @staticmethod
    def get_apps_by_category(loaded_config: Dict[str, Any],
                             category: Optional[str] = None) -> List[App]:
        """
        Get apps, optionally filtered by category

        :param loaded_config: Configuration dictionary from load_from_yaml
        :param category: Optional category to filter by
        :return: List of Apps
        """
        apps = loaded_config['apps']

        if category:
            return [app for app in apps if app.category == category]

        return apps


# Example usage
if __name__ == "__main__":
    # Load entire configuration
    config = AppLoader.load_from_yaml('conf.yml')

    # Get all apps
    all_apps = config['apps']
    print("All Apps:", [app.title for app in all_apps])

    # Get apps by category
    proteomics_apps = AppLoader.get_apps_by_category(config, 'proteomics')
    print("Proteomics Apps:", [app.title for app in proteomics_apps])

    # Print categories
    print("Categories:", config['categories'])