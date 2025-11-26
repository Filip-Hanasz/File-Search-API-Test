import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types


def init_client():
    """Inicjalizacja klienta Gemini API"""
    load_dotenv()
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("Ustaw GEMINI_API_KEY w pliku .env")
    return genai.Client(api_key=api_key)


def create_file_search_store(client):
    """1. Tworzenie nowej biblioteki embeddingów"""
    print("\n=== Tworzenie nowej biblioteki ===")
    display_name = input("Podaj nazwę biblioteki: ")
    
    try:
        file_search_store = client.file_search_stores.create(
            config={'display_name': display_name}
        )
        print(f"✓ Biblioteka utworzona pomyślnie!")
        print(f"  Nazwa: {file_search_store.display_name}")
        print(f"  ID: {file_search_store.name}")
        return file_search_store
    except Exception as e:
        print(f"✗ Błąd podczas tworzenia biblioteki: {e}")
        return None


def list_file_search_stores(client):
    """2. Listowanie wszystkich bibliotek"""
    print("\n=== Lista bibliotek ===")
    
    try:
        stores = list(client.file_search_stores.list())
        
        if not stores:
            print("Brak bibliotek.")
            return []
        
        print(f"\nZnaleziono {len(stores)} bibliotek:\n")
        for i, store in enumerate(stores, 1):
            print(f"{i}. {store.display_name}")
            print(f"   ID: {store.name}")
            print(f"   Utworzona: {store.create_time}")
            print()
        
        return stores
    except Exception as e:
        print(f"✗ Błąd podczas listowania bibliotek: {e}")
        return []


def upload_file_to_store(client):
    """3. Upload pliku do biblioteki"""
    print("\n=== Upload pliku do biblioteki ===")
    
    # Lista bibliotek do wyboru
    stores = list_file_search_stores(client)
    if not stores:
        print("Najpierw utwórz bibliotekę.")
        return
    
    try:
        choice = int(input(f"\nWybierz bibliotekę (1-{len(stores)}): "))
        if choice < 1 or choice > len(stores):
            print("Nieprawidłowy wybór.")
            return
        
        selected_store = stores[choice - 1]
        file_path = input("Podaj ścieżkę do pliku: ")
        
        if not os.path.exists(file_path):
            print("✗ Plik nie istnieje.")
            return
        
        display_name = input("Podaj nazwę wyświetlaną pliku (opcjonalnie, Enter dla nazwy pliku): ")
        if not display_name:
            display_name = os.path.basename(file_path)
        
        print(f"\nUploadowanie pliku '{file_path}' bezpośrednio do biblioteki...")
        
        # Bezpośredni upload do File Search Store (używa tylko File Search API)
        operation = client.file_search_stores.upload_to_file_search_store(
            file=file_path,
            file_search_store_name=selected_store.name,
            config={'display_name': display_name}
        )
        
        print("Oczekiwanie na zakończenie indeksowania...")
        while not operation.done:
            time.sleep(2)
            operation = client.operations.get(operation)
            print(".", end="", flush=True)
        
        print("\n✓ Plik został pomyślnie zindeksowany!")
        print(f"  Biblioteka: {selected_store.display_name}")
        print(f"  Plik: {display_name}")
        
    except ValueError:
        print("✗ Nieprawidłowy wybór.")
    except Exception as e:
        print(f"✗ Błąd podczas uploadu: {e}")


def list_files_in_store(client):
    """4. Listowanie plików w bibliotece"""
    print("\n=== Lista plików w bibliotece ===")
    
    # Lista bibliotek do wyboru
    stores = list_file_search_stores(client)
    if not stores:
        print("Najpierw utwórz bibliotekę.")
        return
    
    try:
        choice = int(input(f"\nWybierz bibliotekę (1-{len(stores)}): "))
        if choice < 1 or choice > len(stores):
            print("Nieprawidłowy wybór.")
            return
        
        selected_store = stores[choice - 1]
        
        print(f"\nDokumenty w bibliotece '{selected_store.display_name}':\n")
        
        # Użycie File Search API do listowania dokumentów w bibliotece
        documents = list(client.file_search_stores.documents.list(
            parent=selected_store.name
        ))
        
        if not documents:
            print("Brak dokumentów w tej bibliotece.")
            return
        
        for i, doc in enumerate(documents, 1):
            display_name = getattr(doc, "display_name", None) or "Bez nazwy"
            mime_type = getattr(doc, "mime_type", "Nieznany")
            size_bytes = getattr(doc, "size_bytes", "Nieznany")
            state = getattr(doc, "state", None)
            create_time = getattr(doc, "create_time", "Nieznany")

            print(f"{i}. {display_name}")
            print(f"   ID: {doc.name}")
            print(f"   Typ: {mime_type}")
            print(f"   Rozmiar: {size_bytes} bajtów")
            if state:
                print(f"   Stan: {state}")
            print(f"   Utworzony: {create_time}")
            print()
        
        return documents
        
    except ValueError:
        print("✗ Nieprawidłowy wybór.")
    except Exception as e:
        print(f"✗ Błąd podczas listowania dokumentów: {e}")
        import traceback
        traceback.print_exc()
        return []


def delete_file(client):
    """5. Kasowanie pliku"""
    print("\n=== Kasowanie pliku ===")
    
    # Lista bibliotek do wyboru
    stores = list_file_search_stores(client)
    if not stores:
        print("Najpierw utwórz bibliotekę.")
        return
    
    try:
        choice = int(input(f"\nWybierz bibliotekę (1-{len(stores)}): "))
        if choice < 1 or choice > len(stores):
            print("Nieprawidłowy wybór.")
            return
        
        selected_store = stores[choice - 1]
        
        print(f"\nDokumenty w bibliotece '{selected_store.display_name}':\n")
        
        # Użycie File Search API do listowania dokumentów w bibliotece
        documents = list(client.file_search_stores.documents.list(
            parent=selected_store.name
        ))
        
        if not documents:
            print("Brak dokumentów do usunięcia w tej bibliotece.")
            return
        
        for i, doc in enumerate(documents, 1):
            display_name = getattr(doc, "display_name", None) or "Bez nazwy"
            print(f"{i}. {display_name}")
        
        doc_choice = int(input(f"\nWybierz dokument do usunięcia (1-{len(documents)}): "))
        if doc_choice < 1 or doc_choice > len(documents):
            print("Nieprawidłowy wybór.")
            return
        
        selected_doc = documents[doc_choice - 1]
        
        display_name = getattr(selected_doc, "display_name", None) or "Bez nazwy"
        confirm = input(f"\nCzy na pewno chcesz usunąć dokument '{display_name}'? (tak/nie): ")
        if confirm.lower() != 'tak':
            print("Anulowano.")
            return
        
        # Usuwanie dokumentu z File Search Store
        # name to pełna nazwa dokumentu: fileSearchStores/{filesearchstore}/documents/{document}
        client.file_search_stores.documents.delete(
            name=selected_doc.name,
            config={'force': True}  # Usuwa wszystkie Chunk i powiązane obiekty
        )
        
        print(f"✓ Dokument '{display_name}' został usunięty z biblioteki.")
        
    except ValueError:
        print("✗ Nieprawidłowy wybór.")
    except Exception as e:
        print(f"✗ Błąd podczas kasowania dokumentu: {e}")
        import traceback
        traceback.print_exc()


def query_model_with_store(client):
    """6. Odpytywanie modelu z użyciem biblioteki"""
    print("\n=== Odpytywanie modelu z biblioteką ===")
    
    # Lista bibliotek do wyboru
    stores = list_file_search_stores(client)
    if not stores:
        print("Najpierw utwórz bibliotekę i dodaj do niej pliki.")
        return
    
    try:
        choice = int(input(f"\nWybierz bibliotekę (1-{len(stores)}): "))
        if choice < 1 or choice > len(stores):
            print("Nieprawidłowy wybór.")
            return
        
        selected_store = stores[choice - 1]
        
        print(f"\nUżywana biblioteka: {selected_store.display_name}")
        question = input("\nZadaj pytanie: ")
        
        if not question.strip():
            print("Pytanie nie może być puste.")
            return
        
        print("\nGenerowanie odpowiedzi...")
        
        # Generowanie odpowiedzi z użyciem File Search Store
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=[selected_store.name]
                        )
                    )
                ]
            )
        )
        
        print("\n" + "="*50)
        print("ODPOWIEDŹ:")
        print("="*50)
        print(response.text)
        print("="*50)
        
        # Wyświetlanie informacji o użytych plikach/embeddingach
        try:
            if hasattr(response, 'candidates') and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                    grounding_metadata = candidate.grounding_metadata
                    
                    print("\n" + "="*50)
                    print("UŻYTE PLIKI/EMBEDDINGI:")
                    print("="*50)
                    
                    # Wyświetlanie grounding_chunks
                    if hasattr(grounding_metadata, 'grounding_chunks') and grounding_metadata.grounding_chunks:
                        print(f"\nZnaleziono {len(grounding_metadata.grounding_chunks)} chunk(ów):\n")
                        for i, chunk in enumerate(grounding_metadata.grounding_chunks, 1):
                            print(f"{i}. Chunk #{i}:")
                            
                            # Sprawdź retrieved_context
                            if hasattr(chunk, 'retrieved_context') and chunk.retrieved_context:
                                ctx = chunk.retrieved_context
                                if hasattr(ctx, 'title') and ctx.title:
                                    print(f"   Tytuł: {ctx.title}")
                                if hasattr(ctx, 'text') and ctx.text:
                                    text_preview = ctx.text[:100] + "..." if len(ctx.text) > 100 else ctx.text
                                    print(f"   Tekst: {text_preview}")
                            
                            # Sprawdź file (jeśli jest)
                            if hasattr(chunk, 'file') and chunk.file:
                                file_info = chunk.file
                                if hasattr(file_info, 'display_name') and file_info.display_name:
                                    print(f"   Plik: {file_info.display_name}")
                                if hasattr(file_info, 'uri') and file_info.uri:
                                    print(f"   URI: {file_info.uri}")
                            
                            # Sprawdź web (jeśli jest)
                            if hasattr(chunk, 'web') and chunk.web:
                                web_info = chunk.web
                                if hasattr(web_info, 'uri') and web_info.uri:
                                    print(f"   URI: {web_info.uri}")
                                if hasattr(web_info, 'title') and web_info.title:
                                    print(f"   Tytuł: {web_info.title}")
                            
                            print()
                    
                    # Wyświetlanie grounding_supports (mapowanie segmentów tekstu do chunków)
                    if hasattr(grounding_metadata, 'grounding_supports') and grounding_metadata.grounding_supports:
                        print(f"\nMapowanie segmentów do chunków ({len(grounding_metadata.grounding_supports)} segment(ów)):\n")
                        for i, support in enumerate(grounding_metadata.grounding_supports, 1):
                            if hasattr(support, 'segment') and support.segment:
                                segment = support.segment
                                if hasattr(segment, 'text') and segment.text:
                                    print(f"  Segment {i}: \"{segment.text}\"")
                            if hasattr(support, 'grounding_chunk_indices') and support.grounding_chunk_indices:
                                indices = support.grounding_chunk_indices
                                print(f"    Używa chunk(ów): {', '.join([f'#{idx+1}' for idx in indices])}")
                            print()
                    
                    print("="*50)
                else:
                    print("\n(Brak metadanych grounding w odpowiedzi)")
        except Exception as e:
            print(f"\n(Uwaga: Nie udało się wyświetlić informacji o plikach: {e})")
        
    except ValueError:
        print("✗ Nieprawidłowy wybór.")
    except Exception as e:
        print(f"✗ Błąd podczas generowania odpowiedzi: {e}")


def main():
    """Główna funkcja aplikacji"""
    try:
        client = init_client()
    except ValueError as e:
        print(f"Błąd: {e}")
        return
    
    while True:
        print("\n" + "="*50)
        print("File Search API - Zarządzanie bibliotekami embeddingów")
        print("="*50)
        print("1. Utwórz nową bibliotekę")
        print("2. Listuj biblioteki")
        print("3. Upload pliku do biblioteki")
        print("4. Listuj pliki w bibliotece")
        print("5. Usuń plik")
        print("6. Odpytaj model z biblioteką")
        print("0. Wyjście")
        print("="*50)
        
        choice = input("\nWybierz opcję: ")
        
        if choice == '1':
            create_file_search_store(client)
        elif choice == '2':
            list_file_search_stores(client)
        elif choice == '3':
            upload_file_to_store(client)
        elif choice == '4':
            list_files_in_store(client)
        elif choice == '5':
            delete_file(client)
        elif choice == '6':
            query_model_with_store(client)
        elif choice == '0':
            print("\nDo widzenia!")
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")


if __name__ == "__main__":
    main()

